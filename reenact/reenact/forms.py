"""Forms for ReEnAct dashboard."""

from __future__ import annotations

from collections import defaultdict

from django.forms import FloatField, Form, NumberInput

from .settings import (
    CATEGORIES,
    SLIDER_DEPENDENCIES,
    SLIDERS,
    SliderConfig,
    SLIDERS_ON_RIGHT_SIDE,
)


def get_max_value(slider: SliderConfig, data: dict | None) -> int | float:
    """
    Get max value for slider based on marsh value in data dict.

    Args:
        slider: The slider configuration object.
        data: Data dictionary containing marsh value.

    Returns:
        int | float: The calculated maximum value for the slider.
    """
    if (
        data is None
        or slider.name not in SLIDER_DEPENDENCIES["densities"]
        or "marsh" not in data
    ):
        return slider.max
    return (
        float(data["marsh"])
        / SLIDER_DEPENDENCIES["marsh_max_area"]
        * SLIDER_DEPENDENCIES["areas_at_full_marsh_usage"][slider.name]
        * SLIDER_DEPENDENCIES["densities"][slider.name]
    )


class CapacitiesForm(Form):
    """
    Form to create sliders from configuration for capacities used in MyPlan.

    Attributes:
        template_name_div (str): Path to the template used for rendering the form.
    """

    template_name_div = "reenact/forms/capacities.html"

    def __init__(self, data=None, **kwargs):
        """
        Initialize the form and dynamically create fields based on SLIDERS configuration.

        Args:
            data: Data to bind to the form.
            **kwargs: Additional keyword arguments for Form initialization.
        """
        self.categories = defaultdict(list)

        for slider in SLIDERS:
            if slider.name in CATEGORIES["production"]:
                self.categories["Erzeugung und Speicherung"].append(slider.name)
            elif slider.name in CATEGORIES["demand"]:
                self.categories["Verbrauch"].append(slider.name)
            else:
                error_msg = f"Slider {slider.name} has no valid category."
                raise KeyError(error_msg)
            field = FloatField(
                label=slider.label,
                help_text=slider.info,
                widget=NumberInput(
                    attrs={
                        "class": "js-range-slider",
                        "data-min": slider.min,
                        "data-max": get_max_value(slider, data),
                        "data-step": slider.step,
                        "data-from": (
                            data.get(slider.name, slider.initial)
                            if data
                            else slider.initial
                        ),
                        "data-skin": "round",
                    },
                ),
            )
            field.unit = slider.unit
            field.icon = f"images/icons/slider_icon_{slider.name}.svg"
            self.base_fields[slider.name] = field

        self.categories = dict(
            self.categories,
        )  # This must be done in order to loop over defaultdict in template

        self.sliders_on_right_side = SLIDERS_ON_RIGHT_SIDE

        super().__init__(data, **kwargs)
