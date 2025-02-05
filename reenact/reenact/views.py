from django.views.generic.base import TemplateView
from . import chart
import json


class MainView(TemplateView):
    template_name = "reenact/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        echarts_option = chart.generate_vertical_echarts_code(chart.production_data, chart.demand_data)
        context["production_demand_chart"]= json.dumps(echarts_option, indent=2)
        return context
