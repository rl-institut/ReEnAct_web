const production = JSON.parse(document.getElementById("production").textContent);
const demand = JSON.parse(document.getElementById("demand").textContent);
const production_my_plan = JSON.parse(document.getElementById("production_my_plan").textContent);
const demand_my_plan = JSON.parse(document.getElementById("demand_my_plan").textContent);
const my_plan_potentials = document.getElementById("my_plan_results").getElementsByClassName("potentials")[0];

const productionDemandChartOptions = generate_main_chart(production, demand, false);
const productionDemandChartMyPlanOptions = generate_main_chart(production_my_plan, demand_my_plan);

create_chart("statusquo-chart", productionDemandChartOptions);
create_chart("scenarios-chart", productionDemandChartOptions);
create_chart("myplan-chart", productionDemandChartMyPlanOptions);

function create_chart(div_id, options) {
    const chartElement = document.getElementById(div_id);
    if (!chartElement)
        return;
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

function reload_chart(div_id) {
    // Reload chart. Useful when size changed, for example after changing tabs. Does not change data.
    const chartElement = document.getElementById(div_id);
    if (!chartElement)
        return;
    try {
        const chart = echarts.getInstanceByDom(chartElement);
        chart.resize();
    } catch (e) {
        // chart not found
    }
}

function update_charts() {
  update_chart("myplan-chart");
  update_potentials_chart();
}

function update_chart(div_id) {
    // Update chart data from form input. Chart options calculated in backend.
    const capacityForm = document.getElementById("capacityForm");
    const formData = new FormData(capacityForm);
    const params = new URLSearchParams(formData).toString();
    fetch(`chart/${div_id}?${params}`).then(
        response => response.json()
    ).then(data => {
        create_chart(div_id, generate_main_chart(data.production, data.demand));
    });
}

function update_potentials_chart() {
  const form = document.getElementById("capacityForm");
  const formData = new FormData(form);
  const params = new URLSearchParams(formData).toString();

  fetch(`/potentials?${params}`)
    .then((response) => response.text())
    .then((text) => {
      my_plan_potentials.innerHTML = text;
    });
}



function generate_main_chart(production, demand, targetLine=true) {
  let totalProduction = production.reduce((sum, item) => sum + item.value, 0);
  let totalDemand = demand.reduce((sum, item) => sum + item.value, 0);

  let seriesList = production.map(prod_item => ({
    name: prod_item.label,
    type: 'bar',
    stack: 'Production',
    data: [prod_item.value, 0],
    itemStyle: { color: prod_item.color }
  }));
  if (seriesList.length > 0) {
    seriesList[0].barCategoryGap = '10%';
    seriesList[0].barWidth = '40%';
    if (targetLine) {
      seriesList[0].markLine = {
        symbol: 'none',
        data: [
          {
            yAxis: 270,
            name: 'Ziel'
          }
        ],
        lineStyle: {
          color: 'gray',
          type: 'dashed'
        },
        label: {
          formatter: 'Ziel: {c}',
          position: 'middle'
        }
      };
    }
  }

  let demandList = demand.map(dem_item => ({
    name: dem_item.label,
    type: 'bar',
    stack: 'Demand',
    data: [0, dem_item.value],
    itemStyle: { color: dem_item.color }
  }));
  if (demandList.length > 0) {
    demandList[0].barGap = '-100%';
    demandList[0].barWidth = '40%';
  }
  seriesList = seriesList.concat(demandList);

  let xaxis_labels = [
    `{bold|${totalProduction.toFixed(1)} GWh} \n Jahreserzeugung`,
    `{bold|${totalDemand.toFixed(1)} GWh} \n Jahresverbrauch`
  ];

  let tooltip_formatter = function(params) {
    let tip = "<table>";
    const demand_labels = demand.map(item => item.label);
    for (const item of params) {
      if (item.dataIndex === 0 && !demand_labels.includes(item.seriesName)) {
        tip += `<tr><td>${item.marker} ${item.seriesName}:</td><td align='right'>${item.value} GWh</td></tr>`;
      }
      if (item.dataIndex === 1 && demand_labels.includes(item.seriesName)) {
        tip += `<tr><td>${item.marker} ${item.seriesName}:</td><td align='right'>${item.value} GWh</td></tr>`;
      }
    }
    tip += "</table>";
    return tip;
  };

  return {
    tooltip: {
    trigger: 'axis',
    formatter: tooltip_formatter,
    axisPointer: {
      type: 'cross',
      label: {
        backgroundColor: '#6a7985'
      }
    }
  },
    grid: { top: '10%', left: '10%', right: '30%', bottom: '15%' },
    xAxis: {
      type: 'category',
      data: xaxis_labels,
      axisLabel: {
        show: true,
        align: 'center',
        rich: {
          bold: {
            fontWeight: "bold",
            fontSize: 16
          }
        }
      },
      axisTick: { show: false },
      axisPointer: {
        show: true,
        label: {
          show:false,
          backgroundColor: '#6a7985',
        }
      }
    },
    yAxis: {
      type: 'value',
      splitLine: { show: true },
      axisLabel: { show: true },
      axisPointer: {
        label: {
          formatter: "{value} GWh",
          backgroundColor: '#6a7985',
        }
      }
    },
    series: seriesList,
    legend: {
      type: "scroll",
      right: '5%',
      orient: 'vertical',
      icon: 'circle',
      textStyle: { fontSize: 12 },
      tooltip: { show: true }
    }
  };
}

function generate_analysis_chart(data) {
  let series = [];
  for (let [k, v] of Object.entries(data.y_data)) {
      series.push({
          name: k,
          data: v,
          type: 'bar',
      });
  }
  for (let [label, target] of Object.entries(data.target || {})) {
      series.push({
          name: label,
          type: 'line',
          markLine: {
              symbol: "none",  // endpoint symbol
              data: [{
                  yAxis: target,
                  lineStyle: {normal: {color: "#000"}}
              }],
          }
      });
  }
  return {
      xAxis: {
          type: 'category',
          data: data.x_data,
          axisLabel: {
              interval: 0,
              rotate: 30,
              //overflow: 'truncate', // or 'break' to continue in a new line
          },
      },
      yAxis: {
          type: 'value',
          name: data.y_label,
          nameLocation: "center",
          nameRotate: 90,
          nameTextStyle: {fontWeight: "bold"},
      },
      tooltip: {},
      legend: {},
      series: series,
  };
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

function fetch_chart(name) {
    // fetch and display scenario data in comparison charts
    let select = document.getElementById('select-' + name);
    let chartElement = document.getElementById('chart-' + name);
    if (!chartElement)
        return;

    // get data from backend
    let request = window.location.origin + '/analysis/' + name + '_chart';
    if (select) {
        // selection: append query
        request = request + '/?q=' + select.value;
    }

    fetch(request, {
        method: 'GET',
        mode: 'cors',
        headers: new Headers({'Accept': 'application/json', 'Content-Type':'text/plain',}),
        credentials: 'same-origin',
    }).then(response => {response.json().then(data => {
        let chart;
        if (echarts.getInstanceByDom(chartElement)) {
            chart = echarts.getInstanceByDom(chartElement);
            chart.clear();
        } else {
            chart = echarts.init(chartElement, null, { renderer: "svg" });
        }
        const options = generate_analysis_chart(data);
        chart.setOption(options);
        chart.resize();
    });}).catch (error => {
        console.log(error);
    });
}
