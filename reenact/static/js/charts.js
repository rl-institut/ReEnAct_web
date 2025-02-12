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
