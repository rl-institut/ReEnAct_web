import json
import time
import logging

from reenact.reenact.settings import (
    SCENARIO_DIR,
    MYPLAN_OEMOF_SCENARIO,
    SLIDERS,
)
from django_oemof import simulation


logger = logging.getLogger()
logger.setLevel(logging.INFO)


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
    parameters = {slider.name: {"capacity": slider.initial} for slider in SLIDERS}
    simulation_id = simulation.simulate_scenario(
        scenario=MYPLAN_OEMOF_SCENARIO,
        parameters=parameters,
    )
    lg_msg = f"Stored initial myplan scenario under simulation ID: {simulation_id}"
    logger.info(lg_msg)


if __name__ == "__main__":
    prerun_initial_myplan_scenario()
