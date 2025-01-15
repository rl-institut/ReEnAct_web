from django.views.generic.base import TemplateView


class MainView(TemplateView):
    template_name = "reenact/index.html"
