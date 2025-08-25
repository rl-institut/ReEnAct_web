"""Module to handle oemof simulation results."""

from __future__ import annotations

from django_oemof.models import Simulation
from reenact.reenact import hooks

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import HttpRequest


def get_simulation_results_from_request(
    scenario: str,
    request: HttpRequest,
) -> int | None:
    """
    Return simulation ID for a given scenario and user input from the request.

    To get results, setup hooks are applied.
    """
    parameters = hooks.set_up_oemof_components_from_user_input("", request.GET)
    return get_simulation_results(scenario, parameters)


def get_simulation_results(scenario: str, parameters: dict) -> int | None:
    """
    Return simulation ID for a given scenario and parameters.

    Return None if no simulation ID is found.
    """
    simulation = Simulation.objects.filter(
        scenario=scenario,
        parameters=parameters,
    ).first()
    return simulation.id if simulation else None
