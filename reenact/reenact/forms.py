from collections import defaultdict

from django.forms import Form
from django.forms import IntegerField
from django.forms import NumberInput

from .settings import SLIDERS, CATEGORIES


class CapacitiesForm(Form):
    template_name_div = "reenact/forms/capacities.html"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.categories = defaultdict(list)

        for slider in SLIDERS:
            if slider.name in CATEGORIES["production"]:
                self.categories["Erzeugung und Speicherung"].append(slider.name)
            elif slider.name in CATEGORIES["demand"]:
                self.categories["Verbrauch"].append(slider.name)
            else:
                error_msg = f"Slider {slider.name} has no valid category."
                raise KeyError(error_msg)
            field = IntegerField(
                label=slider.label,
                help_text=slider.info,
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
            field.unit = slider.unit
            field.icon = f"images/icons/slider_icon_{slider.name}.svg"
            self.fields[slider.name] = field

        self.categories = dict(
            self.categories,
        )  # This must be done in order to loop over defaultdict in template
