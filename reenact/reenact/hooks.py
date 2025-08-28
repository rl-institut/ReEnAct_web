"""Module to apply hooks on oemof simulation."""

import logging
import oemof
import pyomo.environ as po

from .settings import CONFIG
from .forms import CapacitiesForm
from oemof.solph._plumbing import sequence


logger = logging.getLogger(__name__)

EMISSION_CONSTRAINT = 20000000.0


def set_up_oemof_components_from_user_input(
    scenario: str,
    data: dict,
):
    """Set up capacities for volatiles, potentials and load demand amounts from user inputs."""

    # Extract user input
    capacity_form = CapacitiesForm(data=data)
    if not capacity_form.is_valid():
        raise RuntimeError(capacity_form.errors)
    capacities = capacity_form.cleaned_data

    electricity_factor = capacities["mobility"] / 100
    mobility_demand = (
        (1 - electricity_factor) * CONFIG["mobility_demand"]["fossile"]
        + electricity_factor * CONFIG["mobility_demand"]["electric"]
    ) * 1e-3
    parameters = {
        "wind": {"capacity": capacities["wind"], "expandable": False},
        "pv_ground": {"capacity": capacities["pv_ground"], "expandable": False},
        "pv_roof": {"capacity": capacities["pv_roof"], "expandable": False},
        "pv_agri": {"capacity": capacities["pv_agri"], "expandable": False},
        "pv_marsh": {"capacity": capacities["pv_marsh"], "expandable": False},
        "other_biomass": {
            "capacity": (
                capacities["other_biomass"] * CONFIG["other_biomass"]["sb"]
                + capacities["biomass_marsh"] * CONFIG["other_biomass"]["sm"]
            )
            / 1000,
        },
        "electrolyser": {"capacity": capacities["electrolyzer"], "expandable": False},
        "battery": {
            "capacity": capacities["battery"],
            "storage_capacity": capacities["battery"],
            "investment": None,
        },
        "electricity": {"amount": capacities["electricity"]},
        "heat": {"amount": capacities["heat"]},
        "mobility": {"amount": mobility_demand},
        "marsh": capacities["marsh"],
    }
    return parameters


def model_co2_tracking(scenario, data, model):
    if "emissions" not in dir(model):
        flows = {}
        for i, o in model.flows:
            if hasattr(model.flows[i, o], "emission_factor"):
                flows[(i, o)] = model.flows[i, o]

        invest_flows = {}
        for i, o in model.flows:
            if hasattr(model.flows[i, o].investment, "emission_factor"):
                invest_flows[(i, o)] = model.flows[i, o].investment

        invest_storage = {}
        for k in model.es.groups:
            if (
                model.es.groups[k]
                is oemof.solph.components._generic_storage.GenericStorage  # noqa: SLF001
            ):
                if hasattr(model.es.groups[k].investment, "emission_factor"):
                    invest_storage[k] = model.es.groups[k].investment

        model.emissions = po.Expression(
            expr=sum(
                model.flow[inflow, outflow, p, t]
                * model.timeincrement[t]
                * sequence(flows[inflow, outflow].emission_factor)[t]
                for inflow, outflow in flows
                for p, t in model.TIMEINDEX
            )
            + sum(
                model.InvestmentFlowBlock.invest[inflow, outflow, p]
                * invest_flows[inflow, outflow].emission_factor
                for inflow, outflow in invest_flows
                for p in model.PERIODS
            )
            + sum(
                model.GenericInvestmentStorageBlock.invest[model.es.groups[bat], p]
                * invest_storage[bat].emission_factor
                for bat in invest_storage
                for p in model.PERIODS
            ),
        )
    return model


def model_co2_limit(scenario, data, model):
    if "emissions" in dir(model):
        model.emission_constraint = po.Constraint(
            expr=model.emissions <= EMISSION_CONSTRAINT,
        )
    else:
        logger.warning("Emission tracking needed for emission limit.")
    return model


def model_co2_cost(scenario, data, model):
    if "emissions" in dir(model):
        model.objective.set_value(
            expr=model.objective.expr + (0.0 * model.emissions),
        )  # ToDo: cost als variable
    else:
        logger.warning("Emission tracking needed for emission limit.")
    return model


def model_prod_goal(scenario, data, model):
    """ """
    flows = {}
    for i, o in model.flows:
        if str(o) == "el" and "battery" not in str(i) and "import" not in str(i):
            flows[(i, o)] = model.flows[i, o]

    model.el_prod = po.Expression(
        expr=sum(
            model.flow[inflow, outflow, p, t] * model.timeincrement[t]
            for inflow, outflow in flows
            for p, t in model.TIMEINDEX
        ),
    )

    model.el_prod_goal = po.Constraint(expr=model.el_prod >= 0.0)

    return model


def store_emission(scenario: str, data, meta, model):
    meta["emissions"] = model.emissions()
    return meta
