const capacityForm = document.getElementById("capacityForm");

create_main_chart_on_startup();

function createChart(div_id, options) {
  const chartElement = document.getElementById(div_id);
  let chart;
  if (echarts.getInstanceByDom(chartElement)) {
    chart = echarts.getInstanceByDom(chartElement);
    chart.clear();
  } else {
    chart = echarts.init(chartElement, null, { renderer: "svg" });
  }
  chart.setOption(options);
  chart.resize();
}

async function get_echart_options(chartName, parameters) {
    const response = await fetch(`chart/${chartName}?${parameters}`);
    const data = await response.json();
    return data;
}

function create_main_chart() {
    const formData = new FormData(capacityForm);
    const params = new URLSearchParams(formData).toString();
    get_echart_options("main_chart", params).then(
        chartOptions => {createChart("mainChart", chartOptions);},
    );
}

function create_main_chart_on_startup() {
  const productionDemandChartOptions = JSON.parse(document.getElementById("productionDemandChart").textContent);
  createChart("mainChart", productionDemandChartOptions);
}
