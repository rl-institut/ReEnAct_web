from __future__ import annotations

from reenact.reenact import settings
from . import postprocessing
from django_oemof import models


def set_slider(slider):
    return 29.86 + slider * (97.83 / 100)


def thousand_dot(value):
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

    Parameters:
    scenario_data: dict
        A dictionary containing the scenario data, which should include the "boxes"
        key for processing.

    Returns:
    dict[str, float | int | bool]
        A dictionary representing the processed boxes.
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

    Parameters:
    simulation_id: int
        The unique ID for the specific simulation to fetch results for.

    Returns:
    dict
        Holding results for climate, CO2 emissions, cost, and revenue.
    """
    sim = models.Simulation.objects.get(id=simulation_id)
    inputs, outputs = sim.dataset.restore_results()

    prod_goal_achieved = round(postprocessing.prod(inputs, outputs) / 4011, 2)
    co2_amount, co2_cost = postprocessing.co2_ems(inputs, outputs)
    kwh_cost = postprocessing.electricity_price(inputs, outputs)
    inv_cost = postprocessing.invest(inputs, outputs)
    el_rev = postprocessing.el_revenue(inputs, outputs)
    hy_rev = postprocessing.hy_revenue(inputs, outputs)

    boxes = {
        "climate": {
            "percentage": thousand_dot(prod_goal_achieved),
            "total": settings.SCENARIO_GOAL,
            "fulfilled": prod_goal_achieved >= 100.0,  # noqa: PLR2004
        },
        "co2": {
            "emissions": round(co2_amount, 0),
            "cost": round(co2_cost / 1e6, 2),
            "fulfilled": co2_amount == 0,
        },
        "cost": {
            "production": thousand_dot(kwh_cost),
            "invest": round(inv_cost, 2),
        },
        "revenue": {
            "power": thousand_dot(el_rev),
            "hydrogen": thousand_dot(hy_rev),
        },
    }
    return boxes
