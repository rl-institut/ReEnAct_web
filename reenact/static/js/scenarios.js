
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
