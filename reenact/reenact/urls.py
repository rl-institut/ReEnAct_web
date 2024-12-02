from django.urls import path
from django.views.generic.base import TemplateView

from . import views

app_name = "reenact"

urlpatterns = [
    path("", TemplateView.as_view(template_name="reenact/index.html"), name="index"),
    path(
        "infos",
        TemplateView.as_view(template_name="reenact/infos.html"),
        name="infos",
    ),
    path(
        "questionsDefault/regionToday",
        TemplateView.as_view(template_name="reenact/regionToday.html"),
        name="region_today",
    ),
    path("pages/scenario", views.scenario, name="scenario"),
    path(
        "questionsDefault/scenariosOverview",
        TemplateView.as_view(template_name="reenact/scenariosOverview.html"),
        name="scenarios_overview",
    ),
    path(
        "questionsDefault/createScenario",
        TemplateView.as_view(template_name="reenact/createScenario.html"),
        name="create_scenario",
    ),
    path(
        "questionsDefault/scenarioDetail",
        TemplateView.as_view(template_name="reenact/scenarioDetail.html"),
        name="scenario_detail",
    ),
    path(
        "questionsDefault/challenges",
        TemplateView.as_view(template_name="reenact/challenges.html"),
        name="challenges",
    ),
    path(
        "pages/comparison",
        TemplateView.as_view(template_name="reenact/comparison.html"),
        name="comparison",
    ),
    path(
        "source",
        TemplateView.as_view(template_name="reenact/source.html"),
        name="sources",
    ),
    path("help", TemplateView.as_view(template_name="reenact/help.html"), name="help"),
]
