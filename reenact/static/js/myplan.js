
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

function capacitiesChanged() {
  const capacityForm = document.getElementById("capacityForm");
  const formData = new FormData(capacityForm);
  updateURL(formData);
  update_chart("myplan-chart", formData);
  update_potentials();
  capacitiesChangedSimulation();
}

async function capacitiesChangedSimulation() {
  myplanSimulationBtn.disabled = "";
  myplanSimulationBtn.classList.add("animate-popIn");
  myplanSpinner.classList.add("hidden");
  // myplanChartSection.style.opacity = "0.6";
  planChartInputOutput.style.opacity = "0.6";
  componentBox.style.opacity = "0.6";
  // Show update message
  document.querySelectorAll(".myplanUpdateMsg").forEach(element => {
      element.classList.remove("hidden");
      element.innerHTML = msgUpdate;
    }
  );
  myplanSimulationBtn.querySelector(".calculate-button-text").innerText = "Neu berechnen";
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
  update_result_boxes(simulationId);
}

function update_result_boxes(simulationId) {
  fetch(`/boxes?simulation_id=${simulationId}`)
    .then((response) => response.text())
    .then((text) => {
      componentBox.innerHTML = text;
    });
}

function updateURL(formData) {
  const searchParams = new URLSearchParams(formData);
  const newUrl = `${window.location.pathname}?${searchParams.toString()}`;
  window.history.pushState({path: newUrl}, '', newUrl);
}

function copyURLToClipboard() {
  navigator.clipboard.writeText(window.location.href);
  const notification = document.getElementById('copyNotification');
  notification.classList.remove('hidden');
  setTimeout(() => {
    notification.classList.add('hidden');
  }, 2000);
}


window.addEventListener('DOMContentLoaded', () => {
  const invalid_scenario_msg = document.getElementById('invalid_scenario');
  if(invalid_scenario_msg) {
    setTimeout(() => {
      invalid_scenario_msg.classList.add('opacity-0');
    }, 3000);
  }
});
