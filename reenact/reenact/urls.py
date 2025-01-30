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
    path("faq/", TemplateView.as_view(template_name="reenact/faq.html"), name="faq"),
    path(
        "glossary/",
        TemplateView.as_view(template_name="reenact/glossary.html"),
        name="glossary",
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
]
