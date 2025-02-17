function updateScenario(title, description, button) {
    document.querySelectorAll('#scenarioTabs button').forEach(btn => {
        btn.classList.remove("selected");
    });

    button.classList.add("selected");

    if ("content" in document.createElement("template")){
      const scenario_box = document.querySelector("#scenario_box");
      const template = document.querySelector("#scenario_info");

      scenario_box.innerHTML = "";

      const clone = template.content.cloneNode(true);
      let header = clone.querySelector("h2");
      let text = clone.querySelector("p");
      header.textContent = title;
      text.textContent = description;

      scenario_box.appendChild(clone);
   }
}
function select_first_scenario() {
    const firstButton = document.querySelector("#scenarioTabs button");
    if (firstButton) {
        firstButton.click();
    }
}
