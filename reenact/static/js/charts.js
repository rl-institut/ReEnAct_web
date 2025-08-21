const production = JSON.parse(document.getElementById("production").textContent);
const demand = JSON.parse(document.getElementById("demand").textContent);
const production_my_plan = JSON.parse(document.getElementById("production_my_plan").textContent);
const demand_my_plan = JSON.parse(document.getElementById("demand_my_plan").textContent);
const my_plan_potentials = document.getElementById("my_plan_results").getElementsByClassName("potentials")[0];

// Resize charts when switching tabs
document.querySelectorAll("[data-tab]").forEach(tab => tab.addEventListener("click", function () {
  update_all_charts();
}));

const numberFormat = Intl.NumberFormat("de-DE", { maximumFractionDigits: 1 });

const goal2024 = 419.5;

const goalMarkLine = {
  symbol: 'none',
  data: [{
    yAxis: goal2024,
    name: 'Ziel Deutschland (Flächenanteil)'
  }],
  lineStyle: {
    color: 'gray',
    type: 'dashed'
  },
  label: {
    formatter: function(parameters) {return `Erzeugungsziel: ${numberFormat.format(parameters.value)} GWh`;},
    position: 'middle'
  }
};

const productionDemandChartOptions = generate_main_chart(production, demand, false);
const productionDemandChartMyPlanOptions = generate_main_chart(production_my_plan, demand_my_plan);

create_chart("statusquo-chart", productionDemandChartOptions);
create_chart("scenarios-chart", productionDemandChartOptions);
create_chart("myplan-chart", productionDemandChartMyPlanOptions);

function getResponsiveLayout() {
  const width = window.innerWidth;
  if (width >= 1600) {
    return { gridLeft: '10%', gridRight: '40%', legendRight: '5%', axisLabelSize: 24, labelFontSize: 16 };
  } else if (width >= 1280) {
    return { gridLeft: '5%', gridRight: '35%', legendRight: '3%', axisLabelSize: 20, labelFontSize: 14 };
  } else if (width >= 1024) {
    return { gridLeft: '0%', gridRight: '35%', legendRight: '0%', axisLabelSize: 18, labelFontSize: 13 };
  } else {
    return { gridLeft: '0%', gridRight: '15%', legendRight: 'center', axisLabelSize: 16, labelFontSize: 12 }; // or maybe set `show: false` in legend
  }
}

// Function to create a chart with responsive layout
function create_chart(div_id, options) {
  const chartElement = document.getElementById(div_id);
  if (!chartElement) return;

  const { gridLeft, gridRight, legendRight, axisLabelSize, labelFontSize } = getResponsiveLayout();

  options.grid = {
    ...options.grid,
    right: gridRight,
    left: gridLeft,
  };

  options.legend = {
    ...options.legend,
    right: legendRight,
  };

  options.xAxis.axisLabel.rich.bold = {
    ...options.xAxis.axisLabel.rich.bold,
    fontSize: axisLabelSize,
  };

  options.xAxis.axisLabel.rich.label = {
    ...options.xAxis.axisLabel.rich.label,
    fontSize: labelFontSize,
  };

  if (options.series && options.series[0]) {
    options.series[0].markLine = goalMarkLine;
  }

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

function update_chart(div_id, parameters={}) {
    // Update chart data from form input. Chart options calculated in backend.
    const params = new URLSearchParams(parameters).toString();
    fetch(`chart/${div_id}?${params}`).then(
        response => response.json()
    ).then(data => {
        create_chart(div_id, generate_main_chart(data.production, data.demand));
    });
}

// Update all charts on window resize
function update_all_charts() {
  const { gridRight, legendRight } = getResponsiveLayout();
  document.querySelectorAll("[_echarts_instance_]").forEach(element => {
    const chart = echarts.getInstanceByDom(element);
    chart.setOption({
      grid: { right: gridRight },
      legend: { right: legendRight },
    });
    chart.resize();
  });
}

window.addEventListener("resize", update_all_charts);


function update_potentials() {
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
    itemStyle: { color: prod_item.color },
    barCategoryGap: '10%',
    barWidth: '40%'
  }));

  let demandList = demand.map(dem_item => ({
    name: dem_item.label,
    type: 'bar',
    stack: 'Demand',
    data: [0, dem_item.value],
    itemStyle: { color: dem_item.color },
    barGap: '-100%',
    barWidth: '40%'
  }));

  const markLineSeriesElement = {
      // 👇 dummy series for markLine
      type: 'line',
      data: [],  // no bars
      silent: true,  // not interactive
      barGap: '-100%',
      barWidth: '0%',
      markLine: goalMarkLine,
  };
  seriesList = seriesList.concat(demandList);
  seriesList.push(markLineSeriesElement);

  let xaxis_labels = [
    `{bold|${numberFormat.format(totalProduction)} GWh}\n{label|Jahreserzeugung}`,
    `{bold|${numberFormat.format(totalDemand)} GWh}\n{label|Jahresverbrauch}`
  ];

  let tooltip_formatter = function(params) {
    let tip = "<table>";
    const demand_labels = demand.map(item => item.label);
    for (const item of params) {
      if (item.dataIndex === 0 && !demand_labels.includes(item.seriesName)) {
        tip += `<tr><td>${item.marker} ${item.seriesName}:</td><td align='right'>${numberFormat.format(item.value)} GWh</td></tr>`;
      }
      if (item.dataIndex === 1 && demand_labels.includes(item.seriesName)) {
        tip += `<tr><td>${item.marker} ${item.seriesName}:</td><td align='right'>${numberFormat.format(item.value)} GWh</td></tr>`;
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
    grid: { top: '10%', left: '10%', right: '30%', bottom: '20%' },
    xAxis: {
      type: 'category',
      data: xaxis_labels,
      axisLabel: {
        show: true,
        align: 'center',
        rich: {
          bold: {
            fontWeight: "bold",
            fontSize: 24,
            color: '#1e293b',
            lineHeight: 30,
          },
          label: {
            fontWeight: "normal",
            fontSize: 16,
            color: '#64748b',
            lineHeight: 20,
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
      axisLabel: {
        show: true,
        formatter: function(value) {return numberFormat.format(value);}
      },
      axisPointer: {
        label: {
          formatter: function(parameters) {return `${numberFormat.format(parameters.value)} GWh`;},
          backgroundColor: '#6a7985',
        }
      },
      max: function (value) {
          return Math.max(value.max, goal2024);
      }
    },
    series: seriesList,
    legend: {
      type: "scroll",
      right: '0%',
      orient: 'vertical',
      icon: 'circle',
      textStyle: { fontSize: 12 },
      tooltip: { show: true }
    }
  };
}
