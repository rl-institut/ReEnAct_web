def generate_echarts_code(production, demand):
    total_production = sum(item["value"] for item in production)
    total_demand = sum(item["value"] for item in demand)

    series_list = [
        {
            "name": prod_item["label"],
            "type": "bar",
            "stack": "Production",
            "data": [prod_item["value"], 0],
            "itemStyle": {"color": prod_item["color"]},
        }
        for prod_item in production
    ]
    series_list[0]["barCategoryGap"] = "10%"
    series_list[0]["barWidth"] = "40%"

    demand_list = [
        {
            "name": dem_item["label"],
            "type": "bar",
            "stack": "Demand",
            "data": [0, dem_item["value"]],
            "itemStyle": {"color": dem_item["color"]},
        }
        for dem_item in demand
    ]
    demand_list[0]["barGap"] = "-100%"
    demand_list[0]["barWidth"] = "40%"
    series_list.extend(demand_list)

    xaxis_labels = [
        f"{total_production:.1f} MWh \n Jahreserzeugung",
        f"{total_demand:.1f} MWh \n Jahresverbrauch",
    ]

    legend_tooltip_formatter = (
        "function (params) { "
        "  let seriesData = myChart.getOption().series; "
        "  let value = 0; "
        "  seriesData.forEach(series => { "
        "    if (series.name === params.name) { "
        "      value = series.data.find(val => val > 0); "
        "    } "
        "  }); "
        "  return `${params.name}: ${value} MWh`; "
        "}"
    )

    option = {
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {
                "label": False,
                "type": "shadow",
            },
        },
        "textStyle": {
            "rich": {
                "bold": {
                    "fontWeight": "bold",
                    "fontSize": 14,
                    "align": "center",
                },
                "small": {
                    "fontSize": 10,
                    "align": "center",
                },
            },
        },
        "grid": {
            "top": "10%",
            "left": "10%",
            "right": "30%",
            "bottom": "15%",
        },
        "xAxis": {
            "type": "category",
            "data": xaxis_labels,
            "axisLabel": {
                "show": True,
                "align": "center",
            },
            "axisTick": {
                "show": False,
            },
        },
        "yAxis": {
            "type": "value",
            "splitLine": {
                "show": False,
            },
            "axisLabel": {
                "show": False,
            },
        },
        "series": series_list,
        "legend": {
            "right": "5%",
            "orient": "vertical",
            "icon": "circle",
            "textStyle": {
                "fontSize": 12,
            },
            "tooltip": {
                "show": True,
                "formatter": legend_tooltip_formatter,
            },
        },
    }
    return option
