from django.urls import path
from django.views.generic.base import TemplateView

from . import views

app_name = "reenact"

urlpatterns = [
    path(
        "challenges/",
        TemplateView.as_view(template_name="reenact/challenges.html"),
        name="challenges",
    ),
    path(  # GDPR
        "dsgvo/",
        TemplateView.as_view(template_name="reenact/dsgvo.html"),
        name="dsgvo",
    ),
    path(
        "background/",
        TemplateView.as_view(template_name="reenact/background.html"),
        name="background",
    ),
    path(
        "data/",
        TemplateView.as_view(template_name="reenact/data.html"),
        name="data",
    ),
    path(  # legal
        "impressum/",
        TemplateView.as_view(template_name="reenact/impressum.html"),
        name="impressum",
    ),
    path("map/", TemplateView.as_view(template_name="reenact/map.html"), name="map"),
    path(
        "sources/",
        TemplateView.as_view(template_name="reenact/sources.html"),
        name="sources",
    ),
    path("", views.MainView.as_view(), name="index"),
    path("chart/<str:chart_name>/", views.chart, name="chart"),
    path("potentials/", views.PotentialsView.as_view(), name="potentials"),
    path("boxes/", views.ResultBoxView.as_view(), name="boxes"),
    path("scenario/<int:scenario_id>/", views.scenario_chart, name="scenario"),
    path("sliders/<int:scenario_id>/", views.get_sliders_from_scenario, name="sliders"),
]
