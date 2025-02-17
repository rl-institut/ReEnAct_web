function updateScenario(title, description, button) {
    document.querySelectorAll('#scenarioTabs button').forEach(btn => {
        btn.classList.remove("selected");
    });

    button.classList.add("selected");

    document.getElementById("scenarioTitle").textContent = title;
    document.getElementById("scenarioDescription").textContent = description;
}
