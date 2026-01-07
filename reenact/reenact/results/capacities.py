from django_oemof import models

from reenact.reenact.results import postprocessing
from reenact.reenact.settings import (
    COLORS,
    CONFIG,
    FULL_LOAD_HOURS,
    SLIDERS,
    ELECTRICITY_CHART_LABELS,
)


def get_chart_data_from_scenario(scenario_data):
    """
    Get production and demand chart data from scenario data.

    Args:
        scenario_data: Dictionary containing production and demand data.

    Returns:
        dict: A dictionary with 'production' and 'demand' lists of items (label, value, color).
    """
    production = [
        {"label": key, "value": value, "color": COLORS.get(key, "#000000")}
        for key, value in scenario_data["production"].items()
    ]
    demand = [
        {"label": key, "value": value, "color": COLORS.get(key, "#000000")}
        for key, value in scenario_data["demand"].items()
    ]
    return {"production": production, "demand": demand}


def get_electricity_chart_data_from_scenario(scenario_data):
    """
    Get electricity in/out chart data from scenario data.

    Args:
        scenario_data: Dictionary containing el_in and el_out data.

    Returns:
        dict: A dictionary with 'production' and 'demand' lists of items.
    """
    production = [
        {
            "label": ELECTRICITY_CHART_LABELS[key],
            "value": value,
            "color": COLORS.get(ELECTRICITY_CHART_LABELS[key], "#000000"),
        }
        for key, value in scenario_data["el_in"].items()
    ]
    demand = [
        {
            "label": ELECTRICITY_CHART_LABELS[key],
            "value": value,
            "color": COLORS.get(ELECTRICITY_CHART_LABELS[key], "#000000"),
        }
        for key, value in scenario_data["el_out"].items()
    ]
    return {"production": production, "demand": demand}


def get_chart_data_from_oemof_simulation(simulation_id):
    """
    Get chart data from an oemof simulation result.

    Args:
        simulation_id: ID of the simulation.

    Returns:
        dict: Chart data dictionary.
    """
    sim = models.Simulation.objects.get(id=simulation_id)
    results = sim.dataset.restore_results()
    production, demand = postprocessing.gcdfos(*results)
    return get_chart_data_from_scenario({"production": production, "demand": demand})


def get_chart_data_from_user_input(user_input: dict) -> dict:
    """
    Calculate chart data based on user input from sliders.

    Args:
        user_input: Dictionary containing slider values.

    Returns:
        dict: Calculated chart data dictionary.
    """
    production = []
    demand = []

    for slider_config in SLIDERS:
        key = slider_config.name
        label = slider_config.label
        label = "Sonstige Biomasse (BHKW)" if label == "Sonstige Biomasse" else label
        label = "Biomasse Moor (BHKW)" if label == "Biomasse Moor" else label
        category = slider_config.category
        color = COLORS.get(label, "#000000")
        value = float(user_input.get(key, slider_config.initial))
        value = calculate_energy_from_capacity(key, value)

        item = {"label": label, "value": value, "color": color}
        if category == "production":
            production.append(item)
        elif category == "demand":
            demand.append(item)
    return {"production": production, "demand": demand}


def calculate_energy_from_capacity(technology: str, value: float) -> float:
    """
    Calculate energy for technologies using full load hours.

    Args:
        technology: The name of the technology.
        value: The capacity or slider value.

    Returns:
        float: Calculated energy.
    """
    if technology == "mobility":
        # Calculate mobility energy from fossil energy in 2024 and full electric energy in 2040
        electricity_factor = value / 100
        return (
            (1 - electricity_factor) * CONFIG["mobility_demand"]["fossile"]
            + electricity_factor * CONFIG["mobility_demand"]["electric"]
        ) * 1e-3
    if technology in FULL_LOAD_HOURS:
        return value * FULL_LOAD_HOURS[technology] * 1e-3
    return value
