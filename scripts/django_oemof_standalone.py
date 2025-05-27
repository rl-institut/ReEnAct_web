import logging
import time

from django_oemof.standalone import init_django

init_django(installed_apps=["reenact.reenact"])
from django_oemof import simulation  # noqa: E402

logger = logging.getLogger()
logger.setLevel(logging.INFO)

PARAMETERS = {}

start = time.time()
simulation_id = simulation.simulate_scenario(scenario="es6", parameters=PARAMETERS)
lg_msg = f"Simulation Time: {time.time() - start}"
logger.info(lg_msg)
lg_msg = f"Simulation ID: {simulation_id}"
logger.info(lg_msg)
