
## Change/Add Scenarios

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


## Change Slider Properties

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


## Change Background Information

The background information pages are stored as HTML files in `reenact/templates/reenact` and can be altered there.


## Change map layers and legend

### Geodata import 

Geodata used in the application is stored as geopackages (.gpkg) in folder `reenact/data/geodata`.
In order to import this data into the database, a related database model has to be set up in module `reeneact/reenact/models.py`.
The minimum configuration to set up a model is to define the corresponding geopackage filename (without _.gpkg_ suffix) as _data_file_ and 
which layer shall be imported from this geopackage as _layer_.
After setting up migrations and migrating models to database via `python manage.py makemigrations` and `python manage.py migrate` 
(see [Django Migrations](https://docs.djangoproject.com/en/6.0/topics/migrations/) for further information), 
the geodata can be imported to the database using following command:
`make load_data`
This command automatically scans each model defined in models.py, reads-in data from geopackage and imports the data into related table. 

### Map configuration

Map configuration is handled in `config/settings/base.py`.
There, the map setup at startup can be defined by setting the center of the map, the zoom factor and the maximum bounds of the map.
In the _MAP_ENGINE_API_MVTS_ configuration, the layers of the map are defined by setting the layer_id and which model should be used 
(additional details can be set as well). 
In order to (de-) activate the layers on the map, a legend entry must be added for each layer not present at startup.
The legend entry can be added under `reenact/config/geodata_config_exported`. 
The following fields from this config file are used in map legend:
- _name_ references geopackage and layer_id (used in _MAP_ENGINE_API_MVTS_)
- _title_ is used as legend title
- _category_ is used to group layers in legend
- _layer_in_category_order_ can be used to define an order for each layer per category
- _tooltp_text_ is shown when a user hovers to legend info icon next to a layer title
- _color_ is used for legend entry and map layer coloring
