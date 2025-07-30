"""Module to apply hooks on oemof simulation."""

import logging
import oemof
import pyomo.environ as po
from django.http import HttpRequest

from .forms import CapacitiesForm
from .settings import FULL_LOAD_HOURS
from oemof.solph._plumbing import sequence


logger = logging.getLogger(__name__)

EMISSION_CONSTRAINT = 20000000.0


def set_up_oemof_components_from_user_input(
    scenario: str,
    data: dict,
    request: HttpRequest,
):
    """Set up capacities for volatiles, potentials and load demand amounts from user inputs."""

    # Extract user input
    capacity_form = CapacitiesForm(data=data)
    if not capacity_form.is_valid():
        raise RuntimeError(capacity_form.errors)
    capacities = capacity_form.cleaned_data

    parameters = {
        "wind": {"capacity": capacities["wind"], "expandable": False},
        "pv_ground": {"capacity": capacities["pv_ground"], "expandable": False},
        "pv_roof": {"capacity": capacities["pv_roof"], "expandable": False},
        "pv_agri": {"capacity": capacities["pv_agri"], "expandable": False},
        "pv_marsh": {"capacity": capacities["pv_marsh"], "expandable": False},
        "other_biomass": {"capacity": capacities["other_biomass"] / 1000},
        "SB-depot": {"capacity": capacities["biomass_marsh"] / 1000},
        "electrolyser": {"capacity": capacities["electrolyzer"], "expandable": False},
        "battery": {
            "capacity": capacities["battery"],
            "storage_capacity": capacities["battery"],
            "investment": None,
        },
        "electricity": {
            "amount": capacities["electricity"] * FULL_LOAD_HOURS["electricity"],
        },
        "heat": {"amount": capacities["heat"] * FULL_LOAD_HOURS["heat"]},
        "mobility": {"amount": capacities["mobility"] * FULL_LOAD_HOURS["mobility"]},
    }
    return parameters


def model_co2_tracking(scenario, om, request):
    if "emissions" not in dir(om):
        flows = {}
        for i, o in om.flows:
            if hasattr(om.flows[i, o], "emission_factor"):
                flows[(i, o)] = om.flows[i, o]

        invest_flows = {}
        for i, o in om.flows:
            if hasattr(om.flows[i, o].investment, "emission_factor"):
                invest_flows[(i, o)] = om.flows[i, o].investment

        invest_storage = {}
        for k in om.es.groups:
            if (
                om.es.groups[k]
                is oemof.solph.components._generic_storage.GenericStorage  # noqa: SLF001
            ):
                if hasattr(om.es.groups[k].investment, "emission_factor"):
                    invest_storage[k] = om.es.groups[k].investment

        om.emissions = po.Expression(
            expr=sum(
                om.flow[inflow, outflow, p, t]
                * om.timeincrement[t]
                * sequence(flows[inflow, outflow].emission_factor)[t]
                for inflow, outflow in flows
                for p, t in om.TIMEINDEX
            )
            + sum(
                om.InvestmentFlowBlock.invest[inflow, outflow, p]
                * invest_flows[inflow, outflow].emission_factor
                for inflow, outflow in invest_flows
                for p in om.PERIODS
            )
            + sum(
                om.GenericInvestmentStorageBlock.invest[om.es.groups[bat], p]
                * invest_storage[bat].emission_factor
                for bat in invest_storage
                for p in om.PERIODS
            ),
        )
    return om


def model_co2_limit(scenario, om, request):
    if "emissions" in dir(om):
        om.emission_constraint = po.Constraint(expr=om.emissions <= EMISSION_CONSTRAINT)
    else:
        logger.warning("Emission tracking needed for emission limit.")
    return om


def model_co2_cost(scenario, om, request):
    if "emissions" in dir(om):
        om.objective.set_value(
            expr=om.objective.expr + (0.0 * om.emissions),
        )  # ToDo: cost als variable
    else:
        logger.warning("Emission tracking needed for emission limit.")
    return om


def model_prod_goal(scenario, om, request):
    """ """
    flows = {}
    for i, o in om.flows:
        if str(o) == "el" and "battery" not in str(i) and "import" not in str(i):
            flows[(i, o)] = om.flows[i, o]

    om.el_prod = po.Expression(
        expr=sum(
            om.flow[inflow, outflow, p, t] * om.timeincrement[t]
            for inflow, outflow in flows
            for p, t in om.TIMEINDEX
        ),
    )

    om.el_prod_goal = po.Constraint(expr=om.el_prod >= 0.0)

    return om


def store_emission(scenario: str, meta_results, model):
    meta_results["emissions"] = model.emissions()
    return meta_results
