from __future__ import annotations

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
) -> list[dict[str, str | float | int | bool | None]]:
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
    list[dict[str, str | float | int | bool | None]]
        A list of dictionaries representing the processed boxes. Each dictionary contains
        updated values for "value1", "value2", and "slider" fields, along with the other
        existing fields in each box.
    """
    if "boxes" not in scenario_data:
        return []

    boxes = []
    for box in scenario_data["boxes"]:
        box["value1"] = thousand_dot(box["value1"])
        box["value2"] = thousand_dot(box["value2"])
        box["slider"] = set_slider(box["slider"])
        boxes.append(box)
    return boxes


def get_result_boxes_from_oemof_simulation(simulation_id: int) -> list[dict]:
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
    None
    """
    sim = models.Simulation.objects.get(id=simulation_id)
    inputs, outputs = sim.dataset.restore_results()

    prod_goal_achieved = round(postprocessing.prod(inputs, outputs) / 4011, 2)
    co2_amount, co2_cost = postprocessing.co2_ems(inputs, outputs)
    kwh_cost = postprocessing.electricity_price(inputs, outputs)
    inv_cost = postprocessing.invest(inputs, outputs)
    el_rev = postprocessing.el_revenue(inputs, outputs)
    hy_rev = postprocessing.hy_revenue(inputs, outputs)

    boxes = [
        {
            "title": "KLIMAZIELE",
            "value1": thousand_dot(prod_goal_achieved),
            "unit1": "%",
            "subtitle1": "Energieproduktion",
            "info_hover1": "Hier steht Info über Energieproduktion",
            "value2": f"{round(co2_amount, 0)} t / {round(co2_cost / 1e6, 2)} Mio. €",
            "unit2": "",
            "subtitle2": "CO₂ Emissionen / -kosten",
            "info_hover2": "Infos",
        },
        {
            "title": "KOSTEN",
            "value1": thousand_dot(kwh_cost),
            "unit1": "ct/kWh",
            "subtitle1": "Erzeugungspreis",
            "info_hover1": "Hier steht Info über Erzeugungspreis",
            "value2": f"{round(inv_cost, 2)}",
            "unit2": "€",
            "subtitle2": "Investitionsbedarf",
            "info_hover2": "Infos Investitionsbedarf",
        },
        {
            "title": "ERLÖSE",
            "value1": thousand_dot(el_rev),
            "unit1": "€",
            "subtitle1": "Stromexport",
            "info_hover1": "Hier steht Info über Stromexport",
            "value2": f"{thousand_dot(hy_rev)}",
            "unit2": "€",
            "subtitle2": "H₂-Export",
            "info_hover2": "Infos Wasserstoffexport",
        },
    ]
    return boxes
