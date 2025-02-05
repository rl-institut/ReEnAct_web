from django.http import JsonResponse
from django.views.generic.base import TemplateView

from . import settings
from .forms import CapacitiesForm


class MainView(TemplateView):
    template_name = "reenact/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["capacities"] = CapacitiesForm(sliders=settings.SLIDERS)
        return context


def chart(request, chart_name: str) -> JsonResponse:
    """Return echart options as JSON."""
    wind = request.GET.get("wind", 0.0)
    pv = request.GET.get("pv", 0.0)
    dummy_chart = {
        "xAxis": {"type": "category", "data": ["Wind", "Photovoltaik"]},
        "yAxis": {"type": "value"},
        "series": [{"data": [wind, pv], "type": "bar"}],
    }
    return JsonResponse(dummy_chart)
