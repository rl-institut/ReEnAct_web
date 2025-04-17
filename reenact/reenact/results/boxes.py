def set_slider(slider):
    return 29.86 + slider * (97.83 / 100)


def thousand_dot(value):
    try:
        number = int(value)
        return f"{number:,}".replace(",", ".")
    except (ValueError, TypeError):
        return value


def get_result_boxes_from_scenario_data(scenario_data):
    if "boxes" not in scenario_data:
        return []

    boxes = []
    for box in scenario_data["boxes"]:
        box["value1"] = thousand_dot(box["value1"])
        box["value2"] = thousand_dot(box["value2"])
        box["slider"] = set_slider(box["slider"])
        boxes.append(box)
    return boxes
