"""Module to get and aggregate data from oemof datapackages."""

import json

import pandas as pd

from django_oemof import settings


class DatapackageError(Exception):
    """Raised when a datapackage cannot be loaded."""


def check_datapackage(scenario_path):
    """Check if a datapackage can be loaded."""
    if not scenario_path.exists():
        error_msg = (
            f"Unable to find datapackage.json for scenario at '{scenario_path}'."
        )
        raise DatapackageError(error_msg)


def get_potentials(scenario: str) -> dict[str, float]:
    """Get all capacity potentials from oemof datapackage."""
    scenario_path = settings.OEMOF_DIR / scenario
    check_datapackage(scenario_path)

    potentials = {}
    for element in (scenario_path / "data" / "elements").iterdir():
        element_df = pd.read_csv(element)
        if "capacity_potential" in element_df.columns:
            element_df = element_df.set_index("name")
            element_df = element_df.loc[
                element_df["capacity_potential"] != float("inf")
            ]
            potentials.update(element_df["capacity_potential"].to_dict())
    return potentials


def get_full_load_hours(scenario: str) -> dict[str, float]:
    """Get full load hours from oemof datapackage."""
    scenario_path = settings.OEMOF_DIR / scenario
    check_datapackage(scenario_path)

    with (scenario_path / "datapackage.json").open("r", encoding="utf-8") as f:
        datapackage = json.load(f)

    # Gather full load hours by scanning foreign keys in datapackage.json
    full_load_hours = {}
    for resource in datapackage["resources"]:
        if "foreignKeys" not in resource["schema"]:
            continue
        for fk in resource["schema"]["foreignKeys"]:
            if "profile" in fk["reference"]["resource"]:
                timeseries = pd.read_csv(
                    scenario_path
                    / "data"
                    / "sequences"
                    / f"{fk['reference']['resource']}.csv",
                )
                element_df = pd.read_csv(scenario_path / resource["path"])
                for _, row in element_df.iterrows():
                    if row["name"] in full_load_hours:
                        error_msg = (
                            f"Duplicate full load hours for name '{row['name']}' found."
                        )
                        raise KeyError(error_msg)
                    full_load_hours[row["name"]] = timeseries[row[fk["fields"]]].sum()
    return full_load_hours
