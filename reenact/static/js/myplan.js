
const SIMULATION_CHECK_TIME = 5000;  // ms

let currentTask = null;

async function startMyPlan(oemof_scenario) {
  if (currentTask !== null) {
    await stopSimulation(currentTask);
    currentTask = null;
  }
  const parameters = Object.fromEntries(new FormData(document.getElementById("capacityForm")));
  currentTask = await startSimulation(oemof_scenario, parameters);
  setTimeout(checkResults, SIMULATION_CHECK_TIME);
}

async function checkResults() {
  if (currentTask === null) return;
  const simulationId = await checkSimulation(currentTask);
  if (simulationId === null) {
    setTimeout(checkResults, SIMULATION_CHECK_TIME);
  } else {
    showResults(simulationId);
  }
}

function showResults(simulationId) {
  console.log(`Show results for ID #${simulationId}...`);
  update_chart("myplan-chart", {simulationId: simulationId});
}
