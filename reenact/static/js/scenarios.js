const scenario_potentials = document.getElementById("scenario_results").getElementsByClassName("potentials")[0];
const scenario_boxes = document.getElementById("scenario_results").getElementsByClassName("boxes")[0];


function updateScenario(title, description, button, scenarioId) {
    // Alle Buttons deselektieren
    document.querySelectorAll('#scenarioTabs button').forEach(btn => {
        btn.classList.remove("selected");
    });

    // Gewählten Button markieren
    button.classList.add("selected");

    // Titel & Beschreibung aktualisieren
    document.getElementById("scenarioTitle").textContent = title;
    document.getElementById("scenarioDescription").textContent = description;

    loadScenarioChart(scenarioId);
    updateScenarioPotentials(scenarioId);
    updateScenarioResultBoxes(scenarioId);
}

function loadScenarioChart(scenarioId) {
  const request = window.location.origin + '/scenario/' + scenarioId;
  fetch(
    request,
    {
        method: 'GET',
        mode: 'cors',
        headers: new Headers({'Accept': 'application/json', 'Content-Type':'text/plain',}),
        credentials: 'same-origin',
    }
  ).then(
    response => {
      response.json().then(
        data => {
          const options = generate_main_chart(data.production, data.demand);
          create_chart("scenarios-chart", options);
        }
      );
    }
  ).catch (
    error => {
      console.log(error);
    }
  );
}

function updateScenarioPotentials(scenarioId) {
  fetch(`/potentials?scenario=${scenarioId}`, {})
    .then((response) => response.text())
    .then((text) => {
      scenario_potentials.innerHTML = text;
    });
}

function updateScenarioResultBoxes(scenarioId) {
  fetch(`/boxes?scenario=${scenarioId}`, {})
    .then((response) => response.text())
    .then((text) => {
      scenario_boxes.innerHTML = text;
    });
}

function adaptScenarioSliders() {
  const scenarioId = document.querySelector(".scenario-button.selected").innerText.split(":")[0];
  const request = window.location.origin + '/sliders/' + scenarioId;
  fetch(
    request,
    {
        method: 'GET',
        mode: 'cors',
        headers: new Headers({'Accept': 'application/json', 'Content-Type':'text/plain',}),
        credentials: 'same-origin',
    }
  ).then(
    response => {
      response.json().then(
        data => {
          for (const slider_name in data) {
            const value = data[slider_name];
            const slider = $(`#id_${slider_name}`).data('ionRangeSlider');
            slider.update({from: value});
          }
          capacitiesChanged();
          updateColors();
          openTab('myplan');
          update_all_charts();
        }
      );
    }
  ).catch (
    error => {
      console.log(error);
    }
  );
}
