from __future__ import annotations

from django.http import HttpResponse, JsonResponse
from django.views.generic.base import TemplateView
from django_mapengine.views import MapEngineMixin
from django_mapengine.legend import Legend, LegendItem

from reenact.reenact.results import capacities, scenario
from . import settings, hooks
from .forms import CapacitiesForm
from .results import boxes, potentials
from .settings import (
    SCENARIOS,
    MYPLAN_OEMOF_SCENARIO,
    FULL_LOAD_HOURS,
    SLIDER_DATA,
    LABEL_TO_SLIDER,
    LAYERS_BY_CATEGORY,
    LAYERS_BY_NAME,
)

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
        context["capacities"] = CapacitiesForm(self.request.GET)
        if context["capacities"].is_valid():
            # Load potentials and capacity chart from user input
            my_plan_potentials = self.request.GET
            my_plan_capacities = capacities.get_chart_data_from_user_input(
                self.request.GET,
            )
            # Check if simulation exists for user input
            simulation_id = scenario.get_simulation_results_from_request(
                MYPLAN_OEMOF_SCENARIO,
                self.request,
            )
            context["status"] = {"scenario_loaded": True}
            if simulation_id is None:
                context["show_simulation_update_msg"] = True
                context["invalid_scenario_msg"] = (
                    "Die Ergebnisse des Scenarios müssen neu berechnet werden."
                )
        else:
            # User input is not valid, thus default my-plan scenario gets loaded
            if len(self.request.GET) != 0:
                context["invalid_scenario_msg"] = (
                    "Das Scenario konnte nicht geladen werden"
                )
            context["capacities"] = CapacitiesForm()
            my_plan_potentials = {
                name: data["initial"] for name, data in settings.SLIDER_DATA.items()
            }
            initial_capacities = {
                slider.name: round(slider.initial, 0) for slider in settings.SLIDERS
            }
            my_plan_capacities = capacities.get_chart_data_from_user_input(
                initial_capacities,
            )
            parameters = hooks.set_up_oemof_components_from_user_input(
                "",
                initial_capacities,
            )
            simulation_id = scenario.get_simulation_results(
                MYPLAN_OEMOF_SCENARIO,
                parameters,
            )

        context["scenarios"] = settings.SCENARIOS[1:]

        context["potentials_status_quo"] = potentials.add_wetland_potential(
            potentials.get_potentials_from_scenario_data(
                settings.SCENARIOS[0],
            ),
        )

        # Prepare result boxes for statusquo, scenario and myplan
        # at startup statusquo = myplan
        # if simulation_id is given myplan diverges
        context["charts"] = {
            "base": capacities.get_chart_data_from_scenario(SCENARIOS[0]),
            "scenario": capacities.get_chart_data_from_scenario(SCENARIOS[1]),
            "myplan": my_plan_capacities,
        }
        context["charts"]["simulated_scenario"] = (
            capacities.get_electricity_chart_data_from_scenario(SCENARIOS[1])
        )
        if simulation_id is not None:
            context["charts"]["simulated_myplan"] = (
                capacities.get_chart_data_from_oemof_simulation(simulation_id)
            )

        statusquo_box = boxes.get_result_boxes_from_scenario_data(SCENARIOS[0])
        context["results"] = [
            statusquo_box,
            boxes.get_result_boxes_from_scenario_data(SCENARIOS[1]),
        ]

        # Get production and demand for status quo and my plan
        if simulation_id is None:
            context["results"].append(statusquo_box)
        else:
            context["results"].append(
                boxes.get_result_boxes_from_oemof_simulation(simulation_id),
            )

        context["potentials_my_plan"] = potentials.add_wetland_potential(
            potentials.calculate_potentials_from_request(
                my_plan_potentials,
            ),
        )
        context["slider_dependencies"] = settings.SLIDER_DEPENDENCIES
        context["slider_marks"] = settings.SLIDER_MARKS
        context["my_plan_oemof_scenario"] = settings.MYPLAN_OEMOF_SCENARIO
        return context


def chart(request) -> JsonResponse:
    if "simulation_id" in request.GET:
        simulation_id = request.GET["simulation_id"]
        return JsonResponse(
            capacities.get_chart_data_from_oemof_simulation(simulation_id),
        )
    return JsonResponse(capacities.get_chart_data_from_user_input(request.GET))


class PotentialsView(TemplateView):
    """Render HTML for potentials."""

    template_name = "partials/potentials.html"

    def get_context_data(self, **kwargs):
        if "scenario" in self.request.GET:
            scenario_id = int(self.request.GET["scenario"])
            current_potentials = potentials.get_potentials_from_scenario_data(
                SCENARIOS[scenario_id],
            )
        else:
            current_potentials = potentials.calculate_potentials_from_request(
                self.request,
            )
        current_potentials = potentials.add_wetland_potential(current_potentials)
        return {"potentials": current_potentials}


class MapView(TemplateView, MapEngineMixin):
    """Render HTML for map."""

    template_name = "reenact/map.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["mapengine_legend"] = Legend(
            {
                category: [
                    LegendItem(
                        layer["name"].removesuffix(".gpkg"),
                        layer["title"],
                        color=layer["color"],
                        tooltip=layer["tooltip"],
                    )
                    for layer in layers
                    if layer["title"] != "Gemeinden"
                ]
                for category, layers in LAYERS_BY_CATEGORY.items()
            },
        )
        for layer in context["mapengine_layers"]:
            if layer["id"] not in LAYERS_BY_NAME:
                continue
            color_field = (
                "fill-color"
                if "fill-color" in layer["paint"]
                else "circle-color"
                if "circle-color" in layer["paint"]
                else "line-color"
            )
            layer["paint"][color_field] = LAYERS_BY_NAME[layer["id"]]["color"]
        return context


class ResultBoxView(TemplateView):
    """Render HTML for result boxes."""

    template_name = "partials/resultboxes.html"

    def get_context_data(self, **kwargs):
        if "simulation_id" in self.request.GET:
            simulation_id = int(self.request.GET["simulation_id"])
            results = boxes.get_result_boxes_from_oemof_simulation(simulation_id)
            return {"results": results}

        scenario_id = int(self.request.GET["scenario"])
        results = boxes.get_result_boxes_from_scenario_data(SCENARIOS[scenario_id])
        return {"results": results}


def scenario_chart(
    request,
    scenario_id: int,
    *,
    simulated: bool = False,
) -> JsonResponse | HttpResponse:
    """Return echart options as JSON."""
    if request.method != "GET":
        return HttpResponse(status=405)  # wrong method

    if not simulated:
        return JsonResponse(
            capacities.get_chart_data_from_scenario(SCENARIOS[scenario_id]),
        )

    scenario_data = SCENARIOS[scenario_id]
    return JsonResponse(
        capacities.get_electricity_chart_data_from_scenario(scenario_data),
    )


def get_sliders_from_scenario(request, scenario_id: int) -> JsonResponse:
    """Return slider values for given scenario ID."""

    slider_values = {slider: 0 for slider in SLIDER_DATA}
    for slider, value in (
        SCENARIOS[scenario_id]["production"] | SCENARIOS[scenario_id]["demand"]
    ).items():
        if slider not in LABEL_TO_SLIDER:
            continue
        slider_name = LABEL_TO_SLIDER[slider]
        if slider_name not in FULL_LOAD_HOURS:
            continue
        slider_values[slider_name] = round(value * 1000 / FULL_LOAD_HOURS[slider_name])
    return JsonResponse(slider_values)
