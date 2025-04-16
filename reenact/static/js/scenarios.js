const scenario_potentials = document.getElementById("scenario_results").getElementsByClassName("potentials")[0];


function updateScenario(title, description, button) {
    // Alle Buttons deselektieren
    document.querySelectorAll('#scenarioTabs button').forEach(btn => {
        btn.classList.remove("selected");
    });

    // Gewählten Button markieren
    button.classList.add("selected");

    // Titel & Beschreibung aktualisieren
    document.getElementById("scenarioTitle").textContent = title;
    document.getElementById("scenarioDescription").textContent = description;
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
