def prod(inp, outp):
    """
    Sum up local electricity production.
    """
    prod = 0.0

    for k in [
        ("BG-backpressure", "el"),
        ("pv_agri", "el"),
        ("pv_ground", "el"),
        ("pv_marsh", "el"),
        ("pv_roof", "el"),
        ("wind", "el"),
        ("SB-backpressure", "el"),
    ]:
        prod += outp[k]["sequences"]["flow"].sum()

    return prod


def co2_ems(inp, outp):
    """
    Aggregate CO2 emissions and calculate its cost.
    """
    tons = 0.0
    cost = 0.0

    production_goal = 401100  # in MWh # TODO: dynamisieren
    marsh_dry = 5  # in ha # TODO: dynamisieren
    mt_co2_ems = 20  # in t_CO2/ha # TODO: dynamisieren
    produced = prod(inp, outp)
    co2_index = 0.20088  # in t_CO2/MWh # TODO: dynamisieren
    co2_price = 275.0  # in €/t_CO2 # TODO: dynamisieren

    tons = (marsh_dry * mt_co2_ems) + max(0, (production_goal - produced)) * co2_index
    cost = tons * co2_price

    return tons, cost


def electricity_price(inp, outp):  # noqa: C901
    """
    Calculates electricity generation cost (kindof).
    """
    kwh_p = 0.0

    # components involved in electricity aufkommen (erzeugung, import, speicherung)
    ec = [
        ("BG-backpressure", "el"),
        ("pv_agri", "el"),
        ("pv_ground", "el"),
        ("pv_marsh", "el"),
        ("pv_roof", "el"),
        ("wind", "el"),
        ("SB-backpressure", "el"),
        ("EL-import", "el"),
        ("el_sale", "elec"),
        ("BM-gassifier", "bg"),
        ("battery", "None"),
        ("battery", "el"),
        ("el", "battery"),
    ]

    fil = 0.0  # feed-in el-Bus
    costs = 0.0

    # sum up all relevant costs
    for k in ec:
        ic = 0.0
        if "capacity_cost" in inp[k]["scalars"]:
            if outp[k]["scalars"]["invest"] > 0.0:
                ic = outp[k]["scalars"]["invest"] * inp[k]["scalars"]["capacity_cost"]
        elif "investment_ep_costs" in inp[k]["scalars"]:
            if outp[k]["scalars"]["invest"] > 0.0:
                ic = (
                    outp[k]["scalars"]["invest"]
                    * inp[k]["scalars"]["investment_ep_costs"]
                )

        vc = 0.0
        if "variable_costs" in inp[k]["scalars"]:
            if inp[k]["scalars"]["variable_costs"] > 0.0:
                vc = (
                    outp[k]["sequences"]["flow"].sum()
                    * inp[k]["scalars"]["variable_costs"]
                )

        costs += ic + vc

    for v in [
        ("battery", "None"),
        ("battery", "el"),
        ("el", "battery"),
        ("el_sale", "elec"),
        ("BM-gassifier", "bg"),
    ]:
        ec.remove(v)

    # sum up all relevant electricity sources (not battery)
    for k in ec:
        fil += outp[k]["sequences"]["flow"].sum()

    if fil > 0.0:
        kwh_p = 0.1 * costs / fil

    return round(kwh_p, 2)


def invest(inp, outp):
    """
    Sums up all annualized investments.
    """
    inv_c = 0.0

    for k, v in outp.items():
        if "invest" in v["scalars"] and v["scalars"]["invest"] > 0.0:
            tot = 0.0
            if "capacity_cost" in inp[k]["scalars"]:
                tot = v["scalars"]["invest"] * inp[k]["scalars"]["capacity_cost"]
            elif "investment_ep_costs" in inp[k]["scalars"]:
                tot = v["scalars"]["invest"] * inp[k]["scalars"]["investment_ep_costs"]
            inv_c += tot

    return inv_c


def el_revenue(inp, outp):
    """
    Revenue from selling electricity.
    """
    el_rev = 0.0

    if "variable_costs" in inp[("el", "EL-export")]["scalars"]:
        el_rev = (
            inp[("el", "EL-export")]["scalars"]["variable_costs"]
            * outp[("el", "EL-export")]["sequences"]["flow"]
        )
    elif "variable_costs" in inp[("el", "EL-export")]["sequences"]:
        el_rev = (
            inp[("el", "EL-export")]["sequences"]["variable_costs"]
            * outp[("el", "EL-export")]["sequences"]["flow"]
        )

    return round(abs(el_rev.sum()), 2)


def hy_revenue(inp, outp):
    """
    Revenue from selling hydrogen.
    """
    hy_rev = 0.0

    if "variable_costs" in inp[("hy", "HY-export")]["scalars"]:
        hy_rev = (
            inp[("hy", "HY-export")]["scalars"]["variable_costs"]
            * outp[("hy", "HY-export")]["sequences"]["flow"]
        )
    elif "variable_costs" in inp[("hy", "HY-export")]["sequences"]:
        hy_rev = (
            inp[("hy", "HY-export")]["sequences"]["variable_costs"]
            * outp[("hy", "HY-export")]["sequences"]["flow"]
        )

    return round(abs(hy_rev.sum()), 2)


def gcdfos(inp, outp):
    """
    get chart data from oemof simulation
    """
    production = {}
    demand = {}

    # production components
    pc = [
        ("BG-backpressure", "el"),
        ("pv_agri", "el"),
        ("pv_ground", "el"),
        ("pv_marsh", "el"),
        ("pv_roof", "el"),
        ("wind", "el"),
        ("SB-backpressure", "el"),
        ("EL-import", "el"),
    ]
    pc_map = {
        "wind": "Windkraft",
        "EL-import": "Strom-Import",
        "pv_ground": "PV Freiflächen",
        "pv_agri": "PV Agri",
        "pv_marsh": "PV Moor",
        "pv_roof": "PV Dach",
        "SB-backpressure": "Biomasse-BHKW",
        "BG-backpressure": "Biogasanlage",
    }
    # demand components
    dc = [
        ("elec", "EL-heating"),
        ("elec", "electricity"),
        ("elec", "electrolyser"),
        ("elec", "mobility"),
        ("el", "EL-export"),
        ("el", "EL-excess"),
    ]
    dc_map = {
        "EL-excess": "Abregelung",
        "EL-heating": "HH-Wärmeerzeugung",
        "electrolyser": "Elektrolyse",
        "electricity": "HH-Strombedarf",
        "EL-export": "Strom-Export",
        "mobility": "Mobilität",
    }

    for k in pc:
        production[pc_map[k[0]]] = round(outp[k]["sequences"]["flow"].sum(), 2)

    for k in dc:
        demand[dc_map[k[1]]] = round(outp[k]["sequences"]["flow"].sum(), 2)

    return production, demand
