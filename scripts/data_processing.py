import json
import time
import logging

import pathlib
from reenact.reenact.settings import (
    SCENARIO_DIR,
    MYPLAN_OEMOF_SCENARIO,
    SLIDERS,
)
from reenact.reenact import hooks
from django_oemof import simulation

from .ogr_layer_mapping import RelatedModelLayerMapping
from reenact.reenact import models
from django.db.models import Model


GEODATA_DIR = pathlib.Path(__file__).parent.parent / "reenact" / "data" / "geodata"


REGIONS = [
    models.Municipality,
]

# Get all classes defined in models module
MODELS = [
    getattr(models, attr_name)
    for attr_name in dir(models)
    if isinstance(getattr(models, attr_name), type)
    and issubclass(getattr(models, attr_name), Model)
    and attr_name not in ("Model", "Municipality", "StaticRegionModel")
]


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def load_regions(regions: list[Model] | None = None, *, verbose: bool = True) -> None:
    """Load region geopackages into region models."""
    regions = regions or REGIONS
    for region in regions:
        if region.objects.exists():
            log_msg = (
                f"Skipping data for model '{region.__name__}' - "
                f"Please empty model first if you want to update data."
            )
            logging.info(log_msg)
            continue
        log_msg = f"Upload data for region '{region.__name__}'"
        logging.info(log_msg)
        if hasattr(region, "data_folder"):
            data_path = (
                pathlib.Path(GEODATA_DIR)
                / region.data_folder
                / f"{region.data_file}.gpkg"
            )
        else:
            data_path = pathlib.Path(GEODATA_DIR) / f"{region.data_file}.gpkg"
        instance = RelatedModelLayerMapping(
            model=region,
            data=data_path,
            mapping=region.mapping,
            layer=region.layer,
            transform=4326,
        )
        instance.save(strict=True, verbose=verbose)


def load_data(models: list[Model] | None = None) -> None:
    """Load geopackage-based data into models."""
    models = models or MODELS
    for model in models:
        if model.objects.exists():
            log_msg = (
                f"Skipping data for model '{model.__name__}' - "
                f"Please empty model first if you want to update data."
            )
            logging.info(log_msg)
            continue
        log_msg = f"Upload data for model '{model.__name__}'"
        logging.info(log_msg)
        if hasattr(model, "data_folder"):
            data_path = (
                pathlib.Path(GEODATA_DIR)
                / model.data_folder
                / f"{model.data_file}.gpkg"
            )
        else:
            data_path = pathlib.Path(GEODATA_DIR) / f"{model.data_file}.gpkg"
        instance = RelatedModelLayerMapping(
            model=model,
            data=data_path,
            mapping=model.mapping,
            layer=model.layer,
            transform=4326,
        )
        instance.save(strict=True)


def empty_data(models: list[Model] | None = None) -> None:
    """Delete all data from given models."""
    models = models or MODELS
    for model in models:
        model.objects.all().delete()


def prerun_all_scenarios():
    for scenario_file in SCENARIO_DIR.iterdir():
        if scenario_file.suffix != ".json":
            continue
        with scenario_file.open("r", encoding="utf-8") as f:
            scenario = json.load(f)
            oemof_scenario = scenario.get("oemof_scenario", None)
            if oemof_scenario is None:
                continue

            # Run simulation of scenario without parameters
            start = time.time()
            simulation_id = simulation.simulate_scenario(
                scenario=oemof_scenario,
                parameters={},
            )
            lg_msg = f"Simulation Time: {time.time() - start}"
            logger.info(lg_msg)
            lg_msg = f"Simulation ID: {simulation_id}"
            logger.info(lg_msg)


def prerun_initial_myplan_scenario():
    logger.info("Run simulation for initial myplan scenario.")
    parameters = {slider.name: slider.initial for slider in SLIDERS}
    parameters = hooks.set_up_oemof_components_from_user_input("", parameters, None)

    simulation_id = simulation.simulate_scenario(
        scenario=MYPLAN_OEMOF_SCENARIO,
        parameters=parameters,
    )
    lg_msg = f"Stored initial myplan scenario under simulation ID: {simulation_id}"
    logger.info(lg_msg)


if __name__ == "__main__":
    load_data()
