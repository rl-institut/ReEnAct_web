from __future__ import annotations

import math

from reenact.reenact import settings
from reenact.reenact.settings import POTENTIAL_AREAS


def circle_view(arc_percentage):
    radius = 27
    stroke = 2 * math.pi * radius
    stroke_dashoffset = stroke * (1 - arc_percentage / 100)
    return f"{stroke_dashoffset:.5f}"


def calculate_potentials_from_request(request_or_data) -> list:
    if hasattr(request_or_data, "GET"):
        query_data = request_or_data.GET
    else:
        query_data = request_or_data

    potentials = []
    for pot in settings.POTENTIALS:
        raw_value = query_data.get(pot, 0)
        try:
            value = float(raw_value)
        except (TypeError, ValueError):
            value = 0

        potential_data = settings.SLIDER_DATA[pot]
        percentage = (value / potential_data["max"]) * 100
        potentials.append(
            {
                "title": potential_data["label"],
                "percentage": round(percentage),
                "value": round(calculate_area_from_capacity(pot, value)),
                "unit": "km²",
                "color": settings.COLORS[potential_data["label"]],
                "stroke_dashoffset": circle_view(percentage),
            },
        )
    return potentials


def get_potentials_from_scenario_data(scenario_data: dict) -> list:
    if "potentials" not in scenario_data:
        return []

    potentials = []
    for potential_name, potential_data in scenario_data["potentials"].items():
        potentials.append(
            {
                "title": potential_name,
                "percentage": round(potential_data["percentage"]),
                "value": round(potential_data["area"]),
                "unit": "km²",
                "color": settings.COLORS[potential_name],
                "stroke_dashoffset": circle_view(potential_data["percentage"]),
            },
        )
    return potentials


def calculate_area_from_capacity(technology: str, value: float) -> float:
    """Calculate energy for technologies using full load hours."""
    if technology in POTENTIAL_AREAS:
        return value * POTENTIAL_AREAS[technology]
    return value
