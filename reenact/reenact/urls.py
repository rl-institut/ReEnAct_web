from django.urls import path
from django.views.generic.base import TemplateView

from . import views

app_name = "reenact"

urlpatterns = [
    # path('', views.home, name='home'),
    path("", TemplateView.as_view(template_name="reenact/index.html")),
    path("infos", TemplateView.as_view(template_name="reenact/infos.html")),
    path(
        "questionsDefault/regionToday",
        TemplateView.as_view(template_name="reenact/regionToday.html"),
    ),
    path("pages/scenario", views.scenario, name="scenario"),
    path(
        "questionsDefault/scenariosOverview",
        TemplateView.as_view(template_name="reenact/scenariosOverview.html"),
    ),
    path(
        "questionsDefault/createScenario",
        TemplateView.as_view(template_name="reenact/createScenario.html"),
    ),
    path(
        "questionsDefault/scenarioDetail",
        TemplateView.as_view(template_name="reenact/scenarioDetail.html"),
    ),
    path(
        "questionsDefault/challenges",
        TemplateView.as_view(template_name="reenact/challenges.html"),
    ),
    path(
        "pages/comparison",
        TemplateView.as_view(template_name="reenact/comparison.html"),
    ),
    path("source", TemplateView.as_view(template_name="reenact/source.html")),
    path("help", TemplateView.as_view(template_name="reenact/help.html")),
]
