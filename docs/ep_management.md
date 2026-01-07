
### Change/Add Scenarios

All Scenarios are located in the `reenact/reenact/scenarios` folder. 
Scenario with ID _00_ is reserved for status quo scenario, which is only shown on the tab _2024_.
All scenarios starting from ID _01_ are shown on the tab _Szenarien 2045_.
Every scenario contains some basic information like _name_, _title_ and _description_. 
Additionally, every scenario contains static data to build related charts:
- data from _production_ and _demand_ are used in chart _Energiebilanz (einfach)_,
- data from _el_in_ and _el_out_ are used in chart _Strom-Bilanz (vollständig)_,
- data from _potentials_ is used to generate _Genutzte Energieerzeugungsflächen_ and
- data from _boxes_ is used to show values in _Klimaziele_, _Kosten_ and _Erlöse_.

To make use of predefined colors, change or use the technology labels listed in `reenact/reenact/config/colors.json`. 

The first tab (_2024_) only shows a single scenario as baseline - the status quo today. 
When it comes to KPIs, only greenhouse gas emissions and costs are shown. 
Scenarios in the second tab (_Szeanrien 2045_) contain more KPIs as well as a complete electricity balance.


### Change Slider Properties

_Unless otherwise stated, all config JSON files can be found in the folder `reenact/reeanct/config`._

The Sliders are used to set the component capacities in the energy system model. They also alter the basic bar plot,
which shows the amount of produced energy, as well as household consumption. In `sliders.json` you can change the slider
properties, for example its label, min and max value as well as step size.

The conversion factor from sliders setting to amount of energy in the bar plot can be found in `full_load_hours.json`. 
For most of the production (like wind and pv) this means full load hours, others like biomass of mobility are more 
complex. Biomass in tonnes has to be multiplied by heating value and the CHP efficiency. Mobility as is shown here,
consists of the energy amount for the electrified mobility share, as well as the rest, which is still fossil based
and thus less efficient.

A special case is _Wiedervernässung Moore_ which is the requirement for _PV - Moor_ as well as _Biomasse Moor_, and on
top of that, those two are partly competing for the rewetted marshland. These dependencies can be found in 
`marsh_dependencies.json`.

The slider settings also create the used areas. For the area amount the slider setting is multiplied by the factor in
`potential_areas.json`.


### Change Background Information

The background information pages are stored as HTML files in `reenact/templates/reenact` and can be altered there.


### todo: von der karte hab ich keine ahnung

...
