from django.forms import Form
from django.forms import IntegerField
from django.forms import NumberInput

from .settings import SliderConfig


class CapacitiesForm(Form):
    template_name_div = "reenact/forms/capacities.html"

    def __init__(self, sliders: list[SliderConfig]):
        super().__init__()
        for slider in sliders:
            self.fields[slider.name] = IntegerField(
                label=slider.label,
                help_text=slider.unit,
                widget=NumberInput(
                    attrs={
                        "class": "js-range-slider",
                        "data-min": slider.min,
                        "data-max": slider.max,
                        "data-step": slider.step,
                        "data-from": slider.initial,
                        "data-skin": "round",
                    },
                ),
            )
