from django_oemof.results import get_results
from oemof.tabular.postprocessing import calculations, core

from reenact.reenact.settings import (
    CATEGORIES,
    COLORS,
    FULL_LOAD_HOURS,
    SCENARIOS,
    SLIDERS,
    SLIDER_DATA,
)


def get_chart_data_from_scenario(scenario_id):
    scenario_data = SCENARIOS[scenario_id]
    production = [
        {"label": key, "value": value, "color": COLORS.get(key, "#000000")}
        for key, value in scenario_data["production"].items()
    ]
    demand = [
        {"label": key, "value": value, "color": COLORS.get(key, "#000000")}
        for key, value in scenario_data["demand"].items()
    ]
    return {"production": production, "demand": demand}


def get_chart_data_from_oemof_simulation(simulation_id):
    results = get_results(
        simulation_id,
        {
            "production": core.ParametrizedCalculation(
                calculations.AggregatedFlows,
                parameters={"from_nodes": CATEGORIES["production"]},
            ),
            "demand": core.ParametrizedCalculation(
                calculations.AggregatedFlows,
                parameters={"to_nodes": CATEGORIES["demand"]},
            ),
        },
    )
    chart_data = {
        "production": [
            {
                "label": SLIDER_DATA[index[0]]["label"],
                "color": COLORS.get(SLIDER_DATA[index[0]]["label"], "#000000"),
                "value": value * 1e-3,  # in GWh
            }
            for index, value in results["production"].items()
            if index[0] in SLIDER_DATA
        ],
        "demand": [
            {
                "label": SLIDER_DATA[index[1]]["label"],
                "color": COLORS.get(SLIDER_DATA[index[1]]["label"], "#000000"),
                "value": value * 1e-3,  # in GWh
            }
            for index, value in results["demand"].items()
            if index[1] in SLIDER_DATA
        ],
    }
    return chart_data


def get_chart_data_from_user_input(user_input: dict) -> dict:
    production = []
    demand = []

    for slider_config in SLIDERS:
        key = slider_config.name
        label = slider_config.label
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
    """Calculate energy for technologies using full load hours."""
    if technology == "mobility":
        # Calculate mobility energy from fossil energy in 2024 and full electric energy in 2040
        electricity_factor = value / 100
        return (
            (1 - electricity_factor) * 48279.90 + electricity_factor * 7652.15
        ) * 1e-3
    if technology in FULL_LOAD_HOURS:
        return value * FULL_LOAD_HOURS[technology] * 1e-3
    return value
