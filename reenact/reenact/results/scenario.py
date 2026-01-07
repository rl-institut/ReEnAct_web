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

    Args:
        scenario: The name of the oemof scenario.
        request: The HTTP request object containing user input in GET parameters.

    Returns:
        int | None: The ID of the simulation if found, otherwise None.
    """
    parameters = hooks.set_up_oemof_components_from_user_input("", request.GET)
    return get_simulation_results(scenario, parameters)


def get_simulation_results(scenario: str, parameters: dict) -> int | None:
    """
    Return simulation ID for a given oemof scenario and parameters.

    Args:
        scenario: The name of the oemof scenario.
        parameters: A dictionary of parameters used in the simulation.

    Returns:
        int | None: The ID of the simulation if found, otherwise None.
    """
    simulation = Simulation.objects.filter(
        scenario=scenario,
        parameters=parameters,
    ).first()
    return simulation.id if simulation else None
