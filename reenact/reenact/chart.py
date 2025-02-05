import json

def generate_echarts_code(production, demand):
    total_production = sum(item["value"] for item in production)
    total_demand = sum(item["value"] for item in demand)

    series_list = []
    if production:
        first_prod = production[0]
        series_list.append({
            "name": first_prod["label"],
            "type": "bar",
            "barCategoryGap": "10%",
            "barWidth": "40%",
            "stack": "Production",
            "data": [first_prod["value"], 0],
            "itemStyle": {"color": first_prod["color"]}
        })
        for prod_item in production[1:]:
            series_list.append({
                "name": prod_item["label"],
                "type": "bar",
                "stack": "Production",
                "data": [prod_item["value"], 0],
                "itemStyle": {"color": prod_item["color"]}
            })

    if demand:
        first_dem = demand[0]
        series_list.append({
            "name": first_dem["label"],
            "type": "bar",
            "barWidth": "40%",
            "barGap": "-100%",
            "stack": "Demand",
            "data": [0, first_dem["value"]],
            "itemStyle": {"color": first_dem["color"]}
        })
        for dem_item in demand[1:]:
            series_list.append({
                "name": dem_item["label"],
                "type": "bar",
                "stack": "Demand",
                "data": [0, dem_item["value"]],
                "itemStyle": {"color": dem_item["color"]}
            })

    axis_label_formatter = (
        "function (value, index) { "
        f"  return index === 0 "
        f"    ? '{{bold|{total_production:.1f} MWh}}\\n{{small|Jahreserzeugung}}' "
        f"    : '{{bold|{total_demand:.1f} MWh}}\\n{{small|Jahresverbrauch}}'; "
        "}"
    )

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
            "show": True
        },
        "grid": {
            "top": "10%",
            "left": "10%",
            "right": "30%",
            "bottom": "15%"
        },
        "xAxis": {
            "type": "category",
            "data": ["Jahreserzeugung", "Jahresverbrauch"],
            "axisLabel": {
                "formatter": axis_label_formatter,
                "rich": {
                    "bold": {
                        "fontWeight": "bold",
                        "fontSize": 14,
                        "align": "center"
                    },
                    "small": {
                        "fontSize": 10,
                        "align": "center"
                    }
                },
                "align": "center"
            },
            "axisTick": {
                "show": False
            }
        },
        "yAxis": {
            "type": "value",
            "splitLine": {
                "show": False
            },
            "axisLabel": {
                "show": False
            }
        },
        "series": series_list,
        "legend": {
            "right": "5%",
            "orient": "vertical",
            "icon": "circle",
            "textStyle": {
                "fontSize": 12
            },
            "tooltip": {
                "show": True,
                "formatter": legend_tooltip_formatter
            }
        }
    }

    return option


