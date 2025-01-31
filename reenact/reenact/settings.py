from __future__ import annotations

import json
import pathlib
from dataclasses import dataclass

CONFIG_DIR = pathlib.Path(__file__).parent / "config"


@dataclass
class SliderConfig:
    name: str
    label: str
    min: int | float
    max: int | float
    step: int | float
    initial: int | float
    unit: str
    marks: tuple[str, int | float] | None = None


with (CONFIG_DIR / "sliders.json").open("r", encoding="utf-8") as f:
    slider_data = json.load(f)
    SLIDERS = [
        SliderConfig(name=name, **values) for name, values in slider_data.items()
    ]
