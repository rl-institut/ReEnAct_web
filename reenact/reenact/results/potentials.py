from __future__ import annotations

import math

from reenact.reenact import settings
from reenact.reenact.settings import POTENTIAL_AREAS, LABEL_TO_SLIDER, SLIDER_DATA

WETLAND_RELATED_POTENTIALS = ("wet_meadows", "paludiculture", "pv_marsh")


def circle_view(arc_percentage):
    radius = 27
    stroke = 2 * math.pi * radius
    stroke_dashoffset = stroke * (1 - arc_percentage / 100)
    return f"{stroke_dashoffset:.5f}"


def calculate_potentials_from_request(request_or_data) -> list:
    query_data = (
        request_or_data.GET if hasattr(request_or_data, "GET") else request_or_data
    )

    potentials = []
    for pot in settings.POTENTIAL_AREAS:
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
                "percentage": round(min(100, percentage)),
                "value": round(calculate_area_from_capacity(pot, value), 1),
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
                "percentage": round(min(100, potential_data["percentage"])),
                "value": round(potential_data["area"], 1),
                "unit": "km²",
                "color": settings.COLORS[potential_name],
                "stroke_dashoffset": circle_view(potential_data["percentage"]),
            },
        )
    return potentials


def add_wetland_potential(potentials: list[dict]) -> list[dict]:
    """Calculate wetland potentials from usage of paludiculture, PV marsh and wet meadows."""
    area_wetland = 0
    indexes_wetland = []
    for i, potential in enumerate(potentials):
        if LABEL_TO_SLIDER[potential["title"]] in WETLAND_RELATED_POTENTIALS:
            area_wetland += potential["value"]
            indexes_wetland.append(i)
    for i in reversed(indexes_wetland):
        potentials.pop(i)

    total_area = SLIDER_DATA["marsh"]["max"] / 100  # in km2
    percentage = round(area_wetland / total_area * 100)
    potentials.append(
        {
            "title": "Nasswiesen",
            "percentage": min(100, percentage),
            "value": round(area_wetland, 1),
            "unit": "km²",
            "color": settings.COLORS[SLIDER_DATA["marsh"]["label"]],
            "stroke_dashoffset": circle_view(percentage),
        },
    )
    return potentials


def calculate_area_from_capacity(technology: str, value: float) -> float:
    """Calculate energy for technologies using full load hours."""
    if technology in POTENTIAL_AREAS:
        return value * POTENTIAL_AREAS[technology]
    return value
