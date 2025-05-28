import logging
import time

from django_oemof.standalone import init_django

init_django(installed_apps=["reenact.reenact"])
from django_oemof import simulation  # noqa: E402

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def run_simulation(scenario: str, parameters: dict):
    start = time.time()
    simulation_id = simulation.simulate_scenario(
        scenario=scenario,
        parameters=parameters,
    )
    lg_msg = f"Simulation Time: {time.time() - start}"
    logger.info(lg_msg)
    lg_msg = f"Simulation ID: {simulation_id}"
    logger.info(lg_msg)


if __name__ == "__main__":
    _scenario = "es6"
    _parameters = {}
    run_simulation(_scenario, _parameters)
