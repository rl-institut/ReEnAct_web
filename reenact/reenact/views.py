from django.views.generic.base import TemplateView
from django import template
import math

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

        results = [
                {
                "title": "CO2-AUSSTOß",
                  "value1": 14.7,
                  "unit1": "Tonnen",
                  "subtitle1": "Ausstoß",
                  "info_hover1": "Hier steht Info über Ausstoß",
                  "value2":thousand_dot(4042),
                  "unit2":"€",
                  "subtitle2":"Kosten",
                  "info_hover2":"Hier steht Info über Kosten",
                },
                {
                "title": "ENERGIEKOSTEN",
                  "value1": 0.16,
                  "unit1": "€/kWh",
                  "subtitle1": "Erzeugungspreis",
                  "info_hover1": "Hier steht Info über Erzeugungspreis",
                  "value2":thousand_dot(100000),
                  "unit2":"€",
                  "subtitle2":"Investitionsbedarf",
                  "info_hover2":"Hier steht Info über Investitionsbedarf",
                },
                {
                "title": "SELBSTVERSORGUNG",
                  "value1": 114,
                  "unit1": "%",
                  "subtitle1": "Bilanziell",
                  "info_hover1": "Hier steht Info über Bilanziell",
                  "value2": 75,
                  "unit2":"%",
                  "subtitle2":"Zeitgleich",
                  "info_hover2":"Hier steht Info über Zeitgleich",
                }
                ]

        def circle_view(arc_percentage):
            arc_percent = arc_percentage
            radius = 27
            stroke = 2 * math.pi * radius
            stroke_dashoffset = stroke * (1 - arc_percent / 100)
            return stroke_dashoffset

        def set_stroke_dahoffset():
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
                "title": "Nasse Morrbewirtschaftung",
                "percentage": 100,
                "value": 19.5,
                "unit": "km²",
                "color": "#b3de69",
            },
        ]
        set_stroke_dahoffset()

        context["results"] = results
        context["potentials"] = potentials

        return context
