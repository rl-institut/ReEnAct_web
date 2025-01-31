from django.views.generic.base import TemplateView

from . import settings
from .forms import CapacitiesForm


class MainView(TemplateView):
    template_name = "reenact/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["capacities"] = CapacitiesForm(sliders=settings.SLIDERS)
        return context
