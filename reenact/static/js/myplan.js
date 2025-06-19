
/* globals update_chart */

const SIMULATION_CHECK_TIME = 5000;  // ms

let currentTask = null;

const capacityForm = document.getElementById("capacityForm");
const myplanSimulationBtn = document.getElementById("myplanSimulationBtn");
const myplanSpinner = document.getElementById("myplanSpinner");

const msgUpdate = "Die Ergebnisse sind nicht mehr aktuell. Bitte starten Sie die Berechnung neu.";
const msgSimulation = "Berechnung gestartet...";

const msgUpdateColor = "bg-red-300";
const msgSimulationColor = "bg-yellow-300";

async function capacitiesChanged() {
  myplanSimulationBtn.disabled = "";
  myplanSpinner.classList.add("hidden");
  // Show update message
  document.querySelectorAll(".myplanUpdateMsg").forEach(element => {
      element.classList.remove("hidden");
      element.classList.add(msgUpdateColor);
      element.classList.remove(msgSimulationColor);
      element.innerHTML = msgUpdate;
    }
  );
  if (currentTask !== null) {
    await stopSimulation(currentTask);
    currentTask = null;
  }
}

async function startMyPlan(oemof_scenario) {
  myplanSimulationBtn.disabled = "disabled";
  myplanSpinner.classList.remove("hidden");
  // Hide update message
  document.querySelectorAll(".myplanUpdateMsg").forEach(element => {
    element.classList.remove(msgUpdateColor);
    element.classList.add(msgSimulationColor);
    element.innerHTML = msgSimulation;
  });
  if (currentTask !== null) {
    await stopSimulation(currentTask);
    currentTask = null;
  }
  const parameters = Object.fromEntries(new FormData(capacityForm));
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
  myplanSpinner.classList.add("hidden");
  document.querySelectorAll(".myplanUpdateMsg").forEach(element => element.classList.add("hidden"));
  update_chart("myplan-chart", {simulationId: simulationId});  // in charts.js
}
