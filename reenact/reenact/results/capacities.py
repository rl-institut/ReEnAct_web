from reenact.reenact.settings import SCENARIOS, COLORS, SLIDERS, FULL_LOAD_HOURS


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


def get_chart_data_from_user_input(user_input: dict) -> dict:
    production = []
    demand = []

    for slider_config in SLIDERS:
        key = slider_config.name
        label = slider_config.label
        category = slider_config.category
        color = COLORS.get(label, "#cccccc")
        value = float(user_input.get(key, slider_config.initial)) * 1e-3
        value = calculate_energy_from_capacity(key, value)

        item = {"label": label, "value": value, "color": color}
        if category == "production":
            production.append(item)
        elif category == "demand":
            demand.append(item)
    return {"production": production, "demand": demand}


def calculate_energy_from_capacity(technology: str, value: float) -> float:
    """Calculate energy for technologies using full load hours."""
    if technology in FULL_LOAD_HOURS:
        return value * FULL_LOAD_HOURS[technology]
    return value
