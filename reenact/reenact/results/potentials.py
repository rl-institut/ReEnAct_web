from __future__ import annotations

import math

from reenact.reenact import settings
from reenact.reenact.settings import POTENTIAL_AREAS


def calculate_potentials_from_request(request_or_data) -> list:
    def circle_view(arc_percentage):
        radius = 27
        stroke = 2 * math.pi * radius
        stroke_dashoffset = stroke * (1 - arc_percentage / 100)
        return f"{stroke_dashoffset:.5f}"

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


def calculate_area_from_capacity(technology: str, value: float) -> float:
    """Calculate energy for technologies using full load hours."""
    if technology in POTENTIAL_AREAS:
        return value * POTENTIAL_AREAS[technology]
    return value
