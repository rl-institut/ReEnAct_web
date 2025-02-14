const capacityForm = document.getElementById("capacityForm");
const scenariosData = JSON.parse(document.getElementById('scenarios-data').textContent);

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

function generate_main_chart(production, demand) {
  console.log("generate_main_chart in JS aufgerufen");
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
    `${totalProduction.toFixed(1)} MWh \n Jahreserzeugung`,
    `${totalDemand.toFixed(1)} MWh \n Jahresverbrauch`
  ];

  let legendTooltipFormatter = function(params) {
    let chart = echarts.getInstanceByDom(document.getElementById('mainChart'));
    let seriesData = chart.getOption().series;
    let value = 0;
    seriesData.forEach(series => {
      if (series.name === params.name) {
        value = series.data.find(val => val > 0);
      }
    });
    return `${params.name}: ${value} MWh`;
  };

  let option = {
    tooltip: { show: true },
    grid: { top: '10%', left: '10%', right: '30%', bottom: '15%' },
    xAxis: {
      type: 'category',
      data: xaxis_labels,
      axisLabel: { show: true, align: 'center' },
      axisTick: { show: false }
    },
    yAxis: {
      type: 'value',
      splitLine: { show: false },
      axisLabel: { show: false }
    },
    series: seriesList,
    legend: {
      right: '5%',
      orient: 'vertical',
      icon: 'circle',
      textStyle: { fontSize: 12 },
      tooltip: { show: true, formatter: legendTooltipFormatter }
    }
  };

  return option;
}

function update_chart_from_sliders() {
    console.log("update_chart_from_sliders triggered");
    const formData = new FormData(capacityForm);
    const params = new URLSearchParams(formData).toString();
    let requestUrl = window.location.origin + '/chart/main_chart?' + params;

    fetch(requestUrl, {
        method: 'GET',
        mode: 'cors',
        headers: new Headers({
            'Accept': 'application/json',
            'Content-Type': 'text/plain'
        }),
        credentials: 'same-origin',
    })
    .then(response => response.json())
    .then(data => {
        let options = generate_main_chart(data.production, data.demand);
        createChart("mainChart", options);
    })
    .catch(error => console.error("Fehler beim Laden der Chart-Daten:", error));
}

function create_main_chart_on_startup() {
        let requestUrl = window.location.origin + '/chart/main_chart';

    fetch(requestUrl, {
        method: 'GET',
        mode: 'cors',
        headers: new Headers({
            'Accept': 'application/json',
            'Content-Type': 'text/plain'
        }),
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        let options = generate_main_chart(data.production, data.demand);
        createChart("mainChart", options);
    })
    .catch(error => console.error("Fehler beim Laden der Chart-Daten beim Startup:", error));
}

create_main_chart_on_startup();

function reload_main_chart(scenarioNumber) {
    let params = new URLSearchParams({ scenario: scenarioNumber }).toString();
    let requestUrl = window.location.origin + '/chart/main_chart?' + params;

    fetch(requestUrl, {
        method: 'GET',
        mode: 'cors',
        headers: new Headers({
            'Accept': 'application/json',
            'Content-Type': 'text/plain'
        }),
        credentials: 'same-origin',
    })
    .then(response => response.json())
    .then(data => {
        let options = generate_main_chart(data.production, data.demand);
        createChart("mainChart", options);
    })
    .catch(error => console.error("Fehler beim Laden der Szenario-Daten:", error));
}


function reload_chart(name) {
    // fetch and display scenario data in comparison charts
    let select = document.getElementById('select-' + name);
    let chartElement = document.getElementById('chart-' + name);
    if (!chartElement)
        return;

    // get data from backend
    let request = window.location.origin + '/chart/' + name + '_chart';
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
        const options = {
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
        chart.setOption(options);
        chart.resize();
    })}).catch (error => {
        console.log(error);
    });
}
