"""Module to handle oemof simulation results."""

from __future__ import annotations

from django_oemof.models import Simulation


def get_simulation_results(scenario: str, parameters: dict) -> int | None:
    """
    Return simulation ID for given scenario and parameters.

    Return None if no simulation ID is found.
    """
    simulation = Simulation.objects.filter(
        scenario=scenario,
        parameters=parameters,
    ).first()
    return simulation.id if simulation else None
