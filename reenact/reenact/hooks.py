"""Module to apply hooks on oemof simulation."""

from __future__ import annotations

import oemof
import pyomo.environ as po
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import HttpRequest

from .forms import CapacitiesForm
from oemof.solph._plumbing import sequence


def set_up_volatiles(scenario: str, data: dict, request: HttpRequest | None = None):
    """Set up capacities for volatiles."""

    # Extract capacities from user input
    capacity_form = CapacitiesForm(data=data)
    if not capacity_form.is_valid():
        raise RuntimeError(capacity_form.errors)
    capacities = capacity_form.cleaned_data

    parameters = {"wind": {"capacity": capacities["wind"]}}
    return parameters


def track_emissions(scenario: str, model, additional_data):
    """
    Keeps track of CO2 (equivalent) emissions.
    """

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


def store_emission(scenario: str, meta_results, model):
    meta_results["emissions"] = model.emissions()
    return meta_results
