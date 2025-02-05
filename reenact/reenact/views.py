from django.http import JsonResponse
from django.views.generic.base import TemplateView

from . import settings
from .chart import generate_echarts_code
from .forms import CapacitiesForm


class MainView(TemplateView):
    template_name = "reenact/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["capacities"] = CapacitiesForm(sliders=settings.SLIDERS)
        return context


def chart(request, chart_name: str) -> JsonResponse:
    """Return echart options as JSON."""

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

    wind = request.GET.get("wind", 0.0)
    pv = request.GET.get("pv", 0.0)

    for item in production:
        if item["label"] == "Windenergie":
            item["value"] = float(wind)
        elif item["label"] == "Solarenergie":
            item["value"] = float(pv)

    echarts_option = generate_echarts_code(production, demand)
    return JsonResponse(echarts_option)
