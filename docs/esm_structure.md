_The current energy system looks like this:_

![full energy system model](img/full_es8.png?raw=true "Energy System")

Data for all components and feedin and demand inputs for simulating the energy system using oemof.solph can be found within the 
`ReEnAct_web` repository at [reenact/media/oemof/scenario_es](https://github.com/rl-institut/ReEnAct_web/tree/dev/reenact/media/oemof/scenario_es) 


### Energy carriers - `Bus name` (in ES Model)

- Electricity (wholesale market) - `el`
- Electricity (end customer) - `elec`
- Heat - `th`
- Biomass B (direct use in solid CHP) - `sb`
- Biomass A (for Biogas Plant) - `bm`
- Biomass var(-iable) - `bv`
- Biogas (Biogas Plant internal) - `bg`
- Hydrogen - `hy`


### Components - `Component name` (in ES Model)

- Wind - `wind`
- Dach-PV - `pv_roof`
- Freiflächen-PV - `pv_ground`
- Agri-PV - `pv_agri`
- Moor-PV - `pv_marsh`
- Import - `EL-import`
- Battery Storage - `battery`
- Biomass A Depot - `SB-depot`
- variable Biomass Depot - `bio-new`
- Biomass B Depot - `BM-depot`
- Converter A - `BV-variableA`
- Converter B - `BV-variableB`
- Biogas plant: Gassifier - `BM-gassifier`
- Biogas plant: Gas Storage - `BG-storage-bga`
- Biogas plant: CHP (gas) - `BG-backpressure`
- CHP (solid) - `SB-backpressure`
- Electricity Excess - `EL-excess`
- Electricity Export - `EL-export`
- BEV Demand - `mobility`
- Electricity Demand - `electricity`
- Heat Pump - `EL-heating`
- (domestic) Heat Storage - `TH-storage-home`
- Heat Demand - `heat`
- Heat Excess - `TH-excess`
- Electrolyser - `electrolyser`
- Hydrogen Export - `HY-export`


### Units

- `[Energy] = MWh`
- `[Power] = MW`
- `[Emissions (CO2 equiv.)] = Tonnes`
