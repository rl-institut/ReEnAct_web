"""Module containing global settings."""

from __future__ import annotations

import os
import json
import pathlib
import csv
from dataclasses import dataclass
from json import JSONDecodeError
from typing import Any

import yaml

APP_DIR = pathlib.Path(__file__).parent
DATA_DIR = pathlib.Path(__file__).parent.parent / "data"
CONFIG_DIR = APP_DIR / "config"
SCENARIO_DIR = APP_DIR / "scenarios"

MYPLAN_OEMOF_SCENARIO = "scenario_es"
LAYER_CONFIG = CONFIG_DIR / "geodata_config_exported.csv"


with (CONFIG_DIR / "config.yaml").open("r", encoding="utf-8") as f:
    CONFIG = yaml.safe_load(f)


@dataclass
class SliderConfig:
    """Dataclass for slider configuration."""

    name: str
    label: str
    min: int | float
    max: int | float
    step: int | float
    initial: int | float
    unit: str
    marks: list[int | float] | None = None
    category: str | None = None
    info: str | None = None

    def __post_init__(self):
        self.marks = self.marks or []


with (CONFIG_DIR / "sliders.json").open("r", encoding="utf-8") as f:
    SLIDER_DATA = json.load(f)
SLIDERS = [SliderConfig(name=name, **values) for name, values in SLIDER_DATA.items()]
LABEL_TO_SLIDER = {config["label"]: name for name, config in SLIDER_DATA.items()}
LABEL_TO_SLIDER["Sonstige Biomasse (BHKW)"] = "other_biomass"
LABEL_TO_SLIDER["Biomasse Moor (BHKW)"] = "biomass_marsh"
SLIDERS_ON_RIGHT_SIDE = [
    "marsh",
    "pv_marsh",
    "pv_agri",
    "other_biomass",
    "battery",
    "mobility",
]

with (CONFIG_DIR / "categories.json").open("r", encoding="utf-8") as f:
    CATEGORIES = json.load(f)


with (CONFIG_DIR / "colors.json").open("r", encoding="utf-8") as f:
    COLORS = json.load(f)


with (CONFIG_DIR / "marsh_dependencies.json").open("r", encoding="utf-8") as f:
    SLIDER_DEPENDENCIES = json.load(f)

with (CONFIG_DIR / "electricity_chart_labels.json").open("r", encoding="utf-8") as f:
    ELECTRICITY_CHART_LABELS = json.load(f)


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
            try:
                data["number"] = int(scenario_number)
            except ValueError:
                # Skip scenarios without a scenario ID (legacy scenarios)
                continue
            SCENARIOS.append(data)

# If True, scenario data will be loaded from oemof results.
# Otherwise, production and demand data from JSON is used.
USE_SCENARIOS_FROM_SIMULATION = os.environ.get("USE_SCENARIOS_FROM_SIMULATION", False)


with (CONFIG_DIR / "full_load_hours.json").open("r", encoding="utf-8") as f:
    FULL_LOAD_HOURS = json.load(f)

with (CONFIG_DIR / "potential_areas.json").open("r", encoding="utf-8") as f:
    POTENTIAL_AREAS = json.load(f)

SLIDER_MARKS = {
    category: [[item, SLIDER_DATA[item]["marks"]] for item in items]
    for category, items in CATEGORIES.items()
}

SCENARIO_GOAL = 419.5


def get_geodata_config_by_category() -> dict[str, list[dict[str, Any]]]:
    """
    Read geodata_config_exported.csv and return a dict keyed by category.

    Each value is a list of dicts with keys:
      - file_renamed
      - title
      - color
      - tooltip_text
    The list is ordered by numeric 'layer_in_category_order' ascending.

    Returns
    -------
    Dict[str, List[Dict[str, Any]]]
    """

    if not LAYER_CONFIG.exists():
        error_msg = f"Geodata config CSV not found at: {LAYER_CONFIG}"
        raise FileNotFoundError(error_msg)

    by_category: dict[str, list[dict[str, Any]]] = {}

    with LAYER_CONFIG.open("r", encoding="utf-8") as f:
        # The file uses semicolon as delimiter
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            if not row:
                continue
            category = (row.get("category") or "").strip()
            if not category:
                # skip rows without category
                continue
            # Parse order, default large number if missing/unparsable to push to end
            order_raw = (row.get("layer_in_category_order") or "").strip()
            try:
                order_val = float(order_raw) if order_raw != "" else float("inf")
            except ValueError:
                order_val = float("inf")

            item = {
                "name": (row.get("file_renamed") or "").strip(),
                "title": (row.get("title") or "").strip(),
                "color": (row.get("color") or "").strip(),
                "tooltip": (
                    (
                        row.get("tooltip_text")
                        + "<br><br><i>Daten: "
                        + row.get("source")
                        + "</i>"
                    )
                    or ""
                ).strip(),
                "_order": order_val,  # temporary key for sorting
            }
            by_category.setdefault(category, []).append(item)

    # Sort each category list by the stored order and remove the helper key
    for items in by_category.values():
        items.sort(key=lambda x: (x.get("_order", float("inf")), x.get("title", "")))
        for it in items:
            if "_order" in it:
                del it["_order"]

    return by_category


CATEGORY_ORDER = (
    "Grenzen",
    "Erneuerbare Energien heute",
    "EE-Potenziale",
    "Natur und Schutzgebiete",
    "Siedlung und Infrastruktur",
)
LAYERS_BY_CATEGORY = get_geodata_config_by_category()
LAYERS_BY_CATEGORY = dict(
    sorted(LAYERS_BY_CATEGORY.items(), key=lambda x: CATEGORY_ORDER.index(x[0])),
)
LAYERS_BY_NAME = {
    layer["name"].removesuffix(".gpkg"): layer
    for category, layers in LAYERS_BY_CATEGORY.items()
    for layer in layers
}
