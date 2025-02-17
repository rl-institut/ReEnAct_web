from __future__ import annotations

import json
import pathlib
from dataclasses import dataclass

APP_DIR = pathlib.Path(__file__).parent
CONFIG_DIR = APP_DIR / "config"
SCENARIO_DIR = APP_DIR / "scenarios"


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


SCENARIOS = []
for filename in sorted(SCENARIO_DIR.iterdir()):
    if filename.suffix == ".json":
        scenario_id = filename.name.split("_")[0]
        with filename.open("r", encoding="utf-8") as file:
            data = json.load(file)
            data["id"] = int(scenario_id)
            SCENARIOS.append(data)
