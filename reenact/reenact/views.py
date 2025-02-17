from __future__ import annotations

import math
import random

from django.http import HttpResponse, JsonResponse
from django.views.generic.base import TemplateView

from . import settings
from .forms import CapacitiesForm
from .settings import SCENARIOS

production = [
    {"label": "Windenergie", "value": 204.5, "color": "#8dd3c7"},
    {"label": "Solarenergie", "value": 80.6, "color": "#eeee6c"},
    {"label": "Wasserstoff", "value": 20, "color": "#80b1d3"},
    {"label": "Biogas", "value": 40.5, "color": "#bc80bd"},
]

demand = [
    {"label": "Wirtschaft", "value": 204.5, "color": "#f1f5f9"},
    {"label": "Wärmebedarf", "value": 80.6, "color": "#cbd5e1"},
    {"label": "Elektrizität", "value": 80.6, "color": "#64748b"},
    {"label": "Mobilität", "value": 20, "color": "#334155"},
]

def thousand_dot(value):
    """returns formated value"""
    try:
        number = int(value)
        return f"{number:,}".replace(",", ".")
    except (ValueError, TypeError):
        return value

def random_production_color(used_colors):
    """creates random color."""
    while True:
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        if color.lower() not in used_colors:
            return color

def random_gray_color(used_colors):
    """creates random gray color."""
    while True:
        gray_val = random.randint(0x33, 0xCC)
        color = "#{:02x}{:02x}{:02x}".format(gray_val, gray_val, gray_val)
        if color.lower() not in used_colors:
            return color


class MainView(TemplateView):
    template_name = "reenact/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["capacities"] = CapacitiesForm(sliders=settings.SLIDERS)
        context["scenarios"] = settings.SCENARIOS

        def set_slider(slider):
            return 29.86 + slider * (97.83 / 100)

        results = [
            {
                "title": "CO2-AUSSTOß",
                "value1": 14.7,
                "unit1": "Tonnen",
                "subtitle1": "Ausstoß",
                "info_hover1": "Hier steht Info über Ausstoß",
                "value2": thousand_dot(4042),
                "unit2": "€",
                "subtitle2": "Kosten",
                "info_hover2": "Hier steht Info über Kosten",
                "slider": set_slider(1),
            },
            {
                "title": "ENERGIEKOSTEN",
                "value1": 0.16,
                "unit1": "€/kWh",
                "subtitle1": "Erzeugungspreis",
                "info_hover1": "Hier steht Info über Erzeugungspreis",
                "value2": thousand_dot(100000),
                "unit2": "€",
                "subtitle2": "Investitionsbedarf",
                "info_hover2": "Hier steht Info über Investitionsbedarf",
                "slider": set_slider(50),
            },
            {
                "title": "SELBSTVERSORGUNG",
                "value1": 114,
                "unit1": "%",
                "subtitle1": "Bilanziell",
                "info_hover1": "Hier steht Info über Bilanziell",
                "value2": 75,
                "unit2": "%",
                "subtitle2": "Zeitgleich",
                "info_hover2": "Hier steht Info über Zeitgleich",
                "slider": set_slider(100),
            },
        ]

        def circle_view(arc_percentage):
            radius = 27
            stroke = 2 * math.pi * radius
            stroke_dashoffset = stroke * (1 - arc_percentage / 100)
            return f"{stroke_dashoffset:.5f}"

        def set_stroke_dashoffset():
            for pot in potentials:
                pot["stroke_dashoffset"] = circle_view(pot["percentage"])

        potentials = [
            {
                "title": "Windenergie",
                "percentage": 40,
                "value": 12.4,
                "unit": "km²",
                "color": "#8dd3c7",
            },
            {
                "title": "Solarpark",
                "percentage": 82,
                "value": 8.2,
                "unit": "km²",
                "color": "#eeee6c",
            },
            {
                "title": "Dachsolar",
                "percentage": 64,
                "value": 1.9,
                "unit": "km²",
                "color": "#fdb462",
            },
            {
                "title": "Agrisolar",
                "percentage": 100,
                "value": 38.4,
                "unit": "km²",
                "color": "#fb8072",
            },
            {
                "title": "Nasse Moorbewirtschaftung",
                "percentage": 100,
                "value": 19.5,
                "unit": "km²",
                "color": "#b3de69",
            },
        ]
        set_stroke_dashoffset()
        context["results"] = results
        context["potentials"] = potentials

        return context


def chart(request, chart_name: str) -> JsonResponse | HttpResponse:
    """returns raw data (production und demand) as JSON."""
    if request.method != "GET":
        return HttpResponse(status=405)

    if chart_name == "main_chart":
        scenario_param = request.GET.get("scenario")
        if scenario_param:
            try:
                scenario_number = int(scenario_param)
            except ValueError:
                return HttpResponse(status=400)

            scenario = next((s for s in SCENARIOS if s["number"] == scenario_number), None)
            if not scenario:
                return HttpResponse(status=404)

            production_mapping = {
                "wind": {"label": "Windenergie", "color": "#8dd3c7"},
                "pv": {"label": "Solarenergie", "color": "#eeee6c"},
                "biomass": {"label": "Biomasse", "color": "#699434"}
            }
            demand_mapping = {
                "mobility": {"label": "Mobilität", "color": "#334155"},
                "heat": {"label": "Wärmebedarf", "color": "#cbd5e1"},
                "electricity": {"label": "Elektrizität", "color": "#64748b"},
                "h2o": {"label": "Wasser", "color": "#b6b6b6"},

            }

            used_prod_colors = {v["color"].lower() for v in production_mapping.values()}
            used_demand_colors = {v["color"].lower() for v in demand_mapping.values()}

            production_data = []
            for key, value in scenario.get("production", {}).items():
                if key in production_mapping:
                    mapping = production_mapping[key]
                else:
                    mapping = {"label": key.capitalize()}
                    mapping["color"] = random_production_color(used_prod_colors)
                    used_prod_colors.add(mapping["color"].lower())
                production_data.append({
                    "label": mapping["label"],
                    "value": value,
                    "color": mapping["color"],
                })

            demand_data = []
            for key, value in scenario.get("demand", {}).items():
                if key in demand_mapping:
                    mapping = demand_mapping[key]
                else:
                    mapping = {"label": key.capitalize()}
                    mapping["color"] = random_gray_color(used_demand_colors)
                    used_demand_colors.add(mapping["color"].lower())
                demand_data.append({
                    "label": mapping["label"],
                    "value": value,
                    "color": mapping["color"],
                })

            return JsonResponse({"production": production_data, "demand": demand_data})
        else:
            params = request.GET
            updated_production = [item.copy() for item in production]
            if params.get("wind") is not None:
                try:
                    wind_value = float(params.get("wind", 0.0))
                except ValueError:
                    wind_value = 0.0
                for item in updated_production:
                    if item["label"] == "Windenergie":
                        item["value"] = wind_value
            if params.get("pv") is not None:
                try:
                    pv_value = float(params.get("pv", 0.0))
                except ValueError:
                    pv_value = 0.0
                for item in updated_production:
                    if item["label"] == "Solarenergie":
                        item["value"] = pv_value
            return JsonResponse({"production": updated_production, "demand": demand})

    # dummy values for charts, get from DB later
    # structure: scenario name -> scenario data
    data = {
        "Weiter wie bisher": {
            "area": 70,
            "wind": 40,
            "production": 2000,
            "consumption": 7000,
        },
        "Wind-Repowering": {
            "area": 140,
            "wind": 160,
            "production": 8000,
            "consumption": 6000,
        },
        "Zubau PV": {
            "area": 90,
            "wind": 90,
            "production": 5000,
            "consumption": 4000,
        },
        "Zubau Wind und PV": {
            "area": 160,
            "wind": 140,
            "production": 7000,
            "consumption": 5000,
        },
        "Moorbewirtschaftung": {
            "area": 110,
            "wind": 30,
            "production": 1000,
            "consumption": 1000,
        },
        "Wasserstoff": {
            "area": 70,
            "wind": 20,
            "production": 1000,
            "consumption": 1000,
        },
        "Kostenoptimierung": {
            "area": 70,
            "wind": 40,
            "production": 2000,
            "consumption": 1000,
        },
        "Hohe CO2-Preise": {
            "area": 100,
            "wind": 70,
            "production": 3000,
            "consumption": 3000,
        },
        "Suffizienz": {
            "area": 150,
            "wind": 150,
            "production": 7000,
            "consumption": 6000,
        },
        "Autarkie": {"area": 140, "wind": 100, "production": 5000, "consumption": 6000},
        "⭐️ Mein Plan 2040": {
            "area": 130,
            "wind": 100,
            "production": 5000,
            "consumption": 6000,
        },
    }

    if chart_name == "total_chart":
        return JsonResponse(
            {
                "x_data": list(data.keys()),
                "y_data": {  # production and consumption for each scenario
                    "Jahreserzeugung 2040": [
                        v.get("production") for v in data.values()
                    ],
                    "Jahresverbrauch 2040": [
                        v.get("consumption") for v in data.values()
                    ],
                },
                "y_label": "Energieerzeugung und -verbrauch [kWh]",
            },
        )

    if chart_name == "tech_chart":
        technology = request.GET.get("q")
        if technology is None:
            return HttpResponse(status=406)  # not acceptable: technology needed

        return JsonResponse(
            {
                "x_data": list(data.keys()),
                "y_data": {
                    "Installierte Leistung 2040": [
                        v.get(technology) for v in data.values()
                    ],
                },
                "target": {"Ziel 2040": 70},
                "y_label": "Installierte Leistung [MW]",
            },
        )

    if chart_name == "analysis_chart":
        kpi = request.GET.get("q")
        if kpi is None:
            return HttpResponse(status=406)  # not acceptable: KPI needed

        # get label
        labels = {
            "area": "Fläche [km²]",
            "production": "Erzeugung 2040 [MWh]",
            "consumption": "Verbrauch 2040 [MWh]",
        }
        return JsonResponse(
            {
                "x_data": list(data.keys()),
                "y_data": {labels.get(kpi): [v.get(kpi) for v in data.values()]},
            },
        )

    return HttpResponse(status=406)  # not acceptable: unknown chart
