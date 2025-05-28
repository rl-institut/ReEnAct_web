from __future__ import annotations

from django.http import HttpResponse, JsonResponse
from django.views.generic.base import TemplateView

from reenact.reenact.results import capacities, scenario
from . import settings
from .forms import CapacitiesForm
from .results.potentials import (
    calculate_potentials_from_request,
    get_potentials_from_scenario_data,
)
from .results.boxes import get_result_boxes_from_scenario_data
from .settings import SCENARIOS


PRODUCTION = [
    {"label": "Windenergie", "value": 204.5, "color": "#8dd3c7"},
    {"label": "Solarenergie", "value": 80.6, "color": "#eeee6c"},
    {"label": "Wasserstoff", "value": 20, "color": "#80b1d3"},
    {"label": "Biogas", "value": 40.5, "color": "#bc80bd"},
]

DEMAND = [
    {"label": "Wirtschaft", "value": 204.5, "color": "#f1f5f9"},
    {"label": "Wärmebedarf", "value": 80.6, "color": "#cbd5e1"},
    {"label": "Elektrolyseur", "value": 80.6, "color": "#64748b"},
    {"label": "Mobilität", "value": 20, "color": "#334155"},
]


class MainView(TemplateView):
    template_name = "reenact/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["slider_colors"] = {
            slider_config.name: settings.COLORS.get(slider_config.label, "blue")
            for slider_config in settings.SLIDERS
        }
        context["capacities"] = CapacitiesForm(sliders=settings.SLIDERS)
        context["scenarios"] = settings.SCENARIOS

        results = get_result_boxes_from_scenario_data(SCENARIOS[0])
        context["results"] = results

        context["potentials_status_quo"] = get_potentials_from_scenario_data(
            settings.SCENARIOS[0],
        )
        my_plan_potentials = {
            name: data["initial"] for name, data in settings.SLIDER_DATA.items()
        }
        context["potentials_my_plan"] = calculate_potentials_from_request(
            my_plan_potentials,
        )

        # Get production and demand for status quo and my plan
        simulation_id = scenario.get_simulation_results(
            SCENARIOS[0].get("oemof_scenario", ""),
            {},
        )
        if simulation_id is None:
            context.update(capacities.get_chart_data_from_scenario(0))
        else:
            context.update(
                capacities.get_chart_data_from_oemof_simulation(simulation_id),
            )
        my_plan_capacities = capacities.get_chart_data_from_user_input({})
        context["production_my_plan"] = my_plan_capacities["production"]
        context["demand_my_plan"] = my_plan_capacities["demand"]
        return context


def chart(request, chart_name: str) -> JsonResponse:
    return JsonResponse(capacities.get_chart_data_from_user_input(request.GET))


class PotentialsView(TemplateView):
    """Render HTML for potentials."""

    template_name = "partials/potentials.html"

    def get_context_data(self, **kwargs):
        if "scenario" in self.request.GET:
            scenario_id = int(self.request.GET["scenario"])
            potentials = get_potentials_from_scenario_data(SCENARIOS[scenario_id])
        else:
            potentials = calculate_potentials_from_request(self.request)
        return {"potentials": potentials}


class ResultBoxView(TemplateView):
    """Render HTML for result boxes."""

    template_name = "partials/resultboxes.html"

    def get_context_data(self, **kwargs):
        scenario_id = int(self.request.GET["scenario"])
        results = get_result_boxes_from_scenario_data(SCENARIOS[scenario_id])
        return {"results": results}


def analysis(request, chart_name: str) -> JsonResponse | HttpResponse:  # noqa: PLR0911
    if request.method != "GET":
        return HttpResponse(status=405)  # wrong method

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


def scenario_chart(request, scenario_id: int) -> JsonResponse | HttpResponse:
    """Return echart options as JSON."""
    if request.method != "GET":
        return HttpResponse(status=405)  # wrong method
    simulation_id = scenario.get_simulation_results(
        SCENARIOS[scenario_id].get("oemof_scenario", ""),
        {},
    )
    if simulation_id is None:
        return JsonResponse(
            capacities.get_chart_data_from_scenario(scenario_id),
        )
    return JsonResponse(
        capacities.get_chart_data_from_oemof_simulation(simulation_id),
    )
