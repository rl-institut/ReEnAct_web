import math

from django.http import JsonResponse
from django.views.generic.base import TemplateView

from . import settings
from .chart import generate_echarts_code
from .forms import CapacitiesForm


def thousand_dot(value):
    try:
        number = int(value)
        return f"{number:,}".replace(",", ".")
    except (ValueError, TypeError):
        return value


production = [
    {"label": "Windenergie", "value": 204.5, "color": "#1E90FF"},
    {"label": "Solarenergie", "value": 80.6, "color": "#FF7F00"},
    {"label": "Wasserstoff", "value": 20, "color": "#00008B"},
    {"label": "Biogas", "value": 40.5, "color": "#2E8B57"},
]

demand = [
    {"label": "Wirtschaft", "value": 204.5, "color": "#708090"},
    {"label": "Wärmebedarf", "value": 80.6, "color": "#808080"},
    {"label": "Mobilität", "value": 20, "color": "#A9A9A9"},
]


class MainView(TemplateView):
    template_name = "reenact/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["capacities"] = CapacitiesForm(sliders=settings.SLIDERS)

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
        context["production_demand_chart"] = generate_echarts_code(production, demand)
        context["results"] = results
        context["potentials"] = potentials

        return context


def chart(request, chart_name: str) -> JsonResponse:
    """Return echart options as JSON."""

    wind = request.GET.get("wind", 0.0)
    pv = request.GET.get("pv", 0.0)

    for item in production:
        if item["label"] == "Windenergie":
            item["value"] = float(wind)
        elif item["label"] == "Solarenergie":
            item["value"] = float(pv)

    echarts_option = generate_echarts_code(production, demand)
    return JsonResponse(echarts_option)
