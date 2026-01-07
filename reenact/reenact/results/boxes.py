from __future__ import annotations

from reenact.reenact import settings
from . import postprocessing
from django_oemof import models


def set_slider(slider):
    """
    Calculate slider position.

    Args:
        slider: Raw slider value.

    Returns:
        float: Calculated slider position.
    """
    return 29.86 + slider * (97.83 / 100)


def thousand_dot(value):
    """
    Format a number with thousand dots.

    Args:
        value: The value to format.

    Returns:
        str: Formatted string with thousand dots.
    """
    try:
        number = int(value)
        return f"{number:,}".replace(",", ".")
    except (ValueError, TypeError):
        return value


def get_result_boxes_from_scenario_data(
    scenario_data: dict,
) -> dict[str, float | int | bool]:
    """
    Extracts and processes result boxes from the given scenario data.

    This function retrieves the "boxes" data from the provided scenario dictionary,
    processes each box to format specific fields, and returns a list of the modified
    boxes. Fields such as "value1", "value2", and "slider" are transformed using the
    respective helper functions to ensure consistency or apply specific formatting.

    Args:
        scenario_data: A dictionary containing the scenario data, which should
            include the "boxes" key for processing.

    Returns:
        dict[str, float | int | bool]: A dictionary representing the processed boxes.
    """
    if "boxes" not in scenario_data:
        return {}
    return scenario_data["boxes"]


def get_result_boxes_from_oemof_simulation(simulation_id: int) -> dict:
    """
    Retrieves the result boxes from an oemof simulation based on the provided simulation ID.

    This function fetches a specific simulation using its unique ID, restores its dataset results,
    and processes multiple post-simulation assessments. These include checking the production goal achievement,
    calculating CO2 emissions and costs, determining the electricity price, assessing investment needs, and evaluating
    revenues from electricity and hydrogen exports.

    Args:
        simulation_id: The unique ID for the specific simulation to fetch results for.

    Returns:
        dict: Holding results for climate, CO2 emissions, cost, and revenue.
    """
    sim = models.Simulation.objects.get(id=simulation_id)
    inputs, outputs = sim.dataset.restore_results()

    prod_goal_achieved = round(postprocessing.prod(inputs, outputs) / 4195, 2)
    co2_amount, co2_cost = postprocessing.co2_ems(
        inputs,
        outputs,
        sim.parameters["marsh"],
    )
    kwh_cost = postprocessing.electricity_price_new(inputs, outputs)
    inv_cost = postprocessing.fixed_invest(inputs, outputs)
    el_rev = postprocessing.el_revenue(inputs, outputs)
    hy_rev = postprocessing.hy_revenue(inputs, outputs)

    boxes = {
        "climate": {
            "percentage": prod_goal_achieved,
            "total": settings.SCENARIO_GOAL,
            "fulfilled": prod_goal_achieved >= 100.0,  # noqa: PLR2004
        },
        "co2": {
            "emissions": round(co2_amount, 0),
            "cost": round(co2_cost / 1e6, 2),
            "fulfilled": co2_amount == 0,
        },
        "cost": {
            "production": kwh_cost,
            "invest": round(inv_cost, 2),
        },
        "revenue": {
            "power": el_rev,
            "hydrogen": hy_rev,
        },
    }
    return boxes
