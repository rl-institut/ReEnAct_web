from django.views.generic.base import TemplateView
from django import template

register = template.Library()

@register.filter
def thousand_dot(value):
    try:
        number = int(value)
        return f"{number:,}".replace(",", ".")
    except (ValueError, TypeError):
        return value

class MainView(TemplateView):
    template_name = "reenact/index.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        co2_emissions = {
                "title": "CO2-AUSSTOß",
                  "value1": 14.7,
                  "unit1": "Tonnen",
                  "subtitle1": "Ausstoß",
                  "info_hover1": "Hier steht Info über Ausstoß",
                  "value2":thousand_dot(4042),
                  "unit2":"€",
                  "subtitle2":"Kosten",
                  "info_hover2":"Hier steht Info über Kosten",
                  "scale":""}
        energy_costs = {
                "title": "ENERGIEKOSTEN",
                  "value1": 0.16,
                  "unit1": "€/kWh",
                  "subtitle1": "Erzeugungspreis",
                  "info_hover1": "Hier steht Info über Erzeugungspreis",
                  "value2":thousand_dot(100000),
                  "unit2":"€",
                  "subtitle2":"Investitionsbedarf",
                  "info_hover2":"Hier steht Info über Investitionsbedarf",
                  "scale":""}
        self_sufficiency = {
                "title": "SELBSTVERSORGUNG",
                  "value1": 114,
                  "unit1": "%",
                  "subtitle1": "Bilanziell",
                  "info_hover1": "Hier steht Info über Bilanziell",
                  "value2": 75,
                  "unit2":"%",
                  "subtitle2":"Zeitgleich",
                  "info_hover2":"Hier steht Info über Zeitgleich",
                  "scale":""}

        context["co2_emissions"] = co2_emissions
        context["energy_costs"] = energy_costs
        context["self_sufficiency"] = self_sufficiency

        return context
