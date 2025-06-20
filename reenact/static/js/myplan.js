
/* globals update_chart */

const SIMULATION_CHECK_TIME = 5000;  // ms

let currentTask = null;

const capacityForm = document.getElementById("capacityForm");
const myplanSimulationBtn = document.getElementById("myplanSimulationBtn");
const myplanSpinner = document.getElementById("myplanSpinner");
const myplanChartSection = document.getElementById("myplan-chart");
const planChartInputOutput = document.getElementById("plan-chart-input-output");
const componentBox = document.querySelector("#my_plan_results .boxes");

const msgUpdate = "Die Ergebnisse sind nicht mehr aktuell. Bitte starten Sie die Berechnung neu.";
const msgSimulation = "Berechnung gestartet...";

async function capacitiesChanged() {
  myplanSimulationBtn.disabled = "";
  myplanSimulationBtn.classList.add("animate-popIn");
  myplanSpinner.classList.add("hidden");
  myplanChartSection.style.opacity = "0.6";
  planChartInputOutput.style.opacity = "0.6";
  componentBox.style.opacity = "0.6";
  // Show update message
  document.querySelectorAll(".myplanUpdateMsg").forEach(element => {
      element.classList.remove("hidden");
      element.innerHTML = msgUpdate;
    }
  );
  if (currentTask !== null) {
    await stopSimulation(currentTask);
    currentTask = null;
  }
  setTimeout(() => {
    myplanSimulationBtn.classList.remove("animate-popIn");
  }, 300);
}

async function startMyPlan(oemof_scenario) {
  myplanSimulationBtn.disabled = "disabled";
  myplanSpinner.classList.remove("hidden");
  myplanSimulationBtn.querySelector(".calculate-button-text").innerText = "Wird berechnet";
  // Hide update message
  document.querySelectorAll(".myplanUpdateMsg").forEach(element => {
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
  myplanChartSection.style.opacity = "1";
  planChartInputOutput.style.opacity = "1";
  componentBox.style.opacity = "1";
  myplanSimulationBtn.querySelector(".calculate-button-text").innerText = "Neu berechnen";
  document.querySelectorAll(".myplanUpdateMsg").forEach(element => element.classList.add("hidden"));
  update_chart("myplan-chart", {simulationId: simulationId});  // in charts.js
}
