function updateScenario(id, button) {
    document.querySelectorAll('#scenarioTabs button').forEach(btn => {
        btn.classList.remove("selected");
    });

    button.classList.add("selected");

    if ("content" in document.createElement("template")){
      console.log("ID:", id);
      const scenario_box = document.querySelector("#scenario_box");
      let template_name = "#scenario_" + id;
      const template = document.querySelector(template_name);

      scenario_box.innerHTML = "";

      const clone = template.content.cloneNode(true);
      scenario_box.appendChild(clone);
   }
}
function setStartupScenario() {
    const firstButton = document.querySelector("#scenarioTabs button");
    if (firstButton) {
        firstButton.click();
    }
}
