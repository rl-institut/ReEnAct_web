from __future__ import annotations

import json
import pathlib
from dataclasses import dataclass
from json import JSONDecodeError

APP_DIR = pathlib.Path(__file__).parent
CONFIG_DIR = APP_DIR / "config"
SCENARIO_DIR = APP_DIR / "scenarios"

MYPLAN_OEMOF_SCENARIO = "es6"


@dataclass
class SliderConfig:
    name: str
    label: str
    min: int | float
    max: int | float
    step: int | float
    initial: int | float
    unit: str
    mark: int | float | None = None
    category: str | None = None
    info: str | None = None


with (CONFIG_DIR / "sliders.json").open("r", encoding="utf-8") as f:
    SLIDER_DATA = json.load(f)
SLIDERS = [SliderConfig(name=name, **values) for name, values in SLIDER_DATA.items()]
LABEL_TO_SLIDER = {config["label"]: name for name, config in SLIDER_DATA.items()}

with (CONFIG_DIR / "categories.json").open("r", encoding="utf-8") as f:
    CATEGORIES = json.load(f)


with (CONFIG_DIR / "colors.json").open("r", encoding="utf-8") as f:
    COLORS = json.load(f)


with (CONFIG_DIR / "marsh_dependencies.json").open("r", encoding="utf-8") as f:
    SLIDER_DEPENDENCIES = json.load(f)


SCENARIOS = []
for filename in sorted(SCENARIO_DIR.iterdir()):
    if filename.suffix == ".json":
        scenario_number = filename.name.split("_")[0]
        with filename.open("r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except JSONDecodeError as e:
                error_msg = f"Could not load scenario {filename} due to JSON error."
                raise RuntimeError(error_msg) from e
            data["number"] = int(scenario_number)
            SCENARIOS.append(data)


with (CONFIG_DIR / "full_load_hours.json").open("r", encoding="utf-8") as f:
    FULL_LOAD_HOURS = json.load(f)

with (CONFIG_DIR / "potential_areas.json").open("r", encoding="utf-8") as f:
    POTENTIAL_AREAS = json.load(f)

SLIDER_MARKS = {
    category: [
        [item, SLIDER_DATA[item]["mark"]]
        for item in items
        if SLIDER_DATA[item].get("mark", None)
    ]
    for category, items in CATEGORIES.items()
}
