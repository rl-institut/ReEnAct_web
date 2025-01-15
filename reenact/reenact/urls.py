from django.urls import path

from . import views

app_name = "reenact"

urlpatterns = [
    path("", views.MainView.as_view(), name="index"),
]
