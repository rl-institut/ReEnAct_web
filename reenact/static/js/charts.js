const productionDemandChartOptions = JSON.parse(document.getElementById("productionDemandChart").textContent);

create_chart("statusquo-chart", productionDemandChartOptions);
create_chart("scenarios-chart", productionDemandChartOptions);
create_chart("myplan-chart", productionDemandChartOptions);

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

function update_chart(div_id) {
    // Update chart data from form input. Chart options calculated in backend.
    const capacityForm = document.getElementById("capacityForm");
    const formData = new FormData(capacityForm);
    const params = new URLSearchParams(formData).toString();
    fetch(`chart/${div_id}?${params}`).then(
        response => response.json()
    ).then(chartOptions => {
        create_chart(div_id, chartOptions);
    });
}

function init_chart(divId) {
  const chartElement = document.getElementById(divId);
    if (!chartElement) {
      throw new Error(`Failed to initialize chart. Chart div '${divId}' cannot be found.`);
    }
  let chart;
  if (echarts.getInstanceByDom(chartElement)) {
        chart = echarts.getInstanceByDom(chartElement);
        chart.clear();
    } else {
        chart = echarts.init(chartElement, null, { renderer: "svg" });
    }
  return chart;
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
          const chart = init_chart("scenarios-chart");
          chart.setOption(data);
          chart.resize();
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
    });}).catch (error => {
        console.log(error);
    });
}
