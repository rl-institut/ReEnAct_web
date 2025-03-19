from .settings import SCENARIOS, COLORS


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
