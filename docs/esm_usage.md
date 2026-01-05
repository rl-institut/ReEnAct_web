All energy systems can be found in the `reenact/media/oemof` folder.

### Tabular Energy System File Structure

_If you want to run a tabular energy system, its file structure needs to look like this:_

```
├── es_top_folder
│   ├── data
│   │   ├── elements
│   │   │   ├── bus.csv
│   │   │   ├── ...
│   │   ├── sequences
│   │   │   ├── profile.csv
│   │   │   ├── ...
│   ├── scripts
│   │   ├── build_datapackage.py
│   │   ├── ...
│   ├── datapackage.json
```

- `data/elements` contains all of you parameterized components as csv-files
- `data/sequences` contains all of you time series data
- `scripts` contains datapackage specific python scripts, that you might need
- `datapackage.json` contains the ES structure and has to be copied/generated

### Working on an Energy System

If you want to change energy system parameters or create a new energy system, you look into the existing energy system folders or create a new one respectively.
For ReEnAct, the most relevant energy system is `sceanrio_es`.

To change component parameters (like investment costs or generation capacity) change the corresponding cell in the csv-file. To
alter the structure of the energy system, make the changes in all the necessary csv-files. If you want to add components, that
are not currently included, look at the [components that tabular provides](https://oemof-tabular.readthedocs.io/en/stable/reference/oemof.tabular.html).

There and also [here](https://oemof-tabular.readthedocs.io/en/latest/facades.html) you can get an overview of required and optional component parameters, as well as default values.

After creating an Energy System and to run the optimization, you first need to build the `datapackage.json` by running `python path/to/scripts/build_datpackage.py`

### Simulation and Postprocessing via Script

**Important: energy import and export prices must be set statically or a dynamic price timeseries has to be added / altered.**

To run a simulation without running the full energy planner app, `django_oemof_standalone.py` in the scripts folder can be used.
To access simulation results, the database object can be accessed via `sim = models.Simulation.objects.get(id=cid)` and 
from it, input and output dicts can be accessed via `inputs, outputs = sim.dataset.restore_results()`. You need to
do `from django_oemof import models` first for this.

If you want to utilize the postprocessing functions, you can import and use them like this:

```

# add this to the imports:
from reenact.reenact.results.postprocessing import (
    prod,
    co2_ems,
    electricity_price_new,
    fixed_invest,
    el_revenue,
    hy_revenue,
    gcdfos,
)

# and (if you for example want to plot the KPIs) add this to the main function:
    print(f"prod: {prod(inputs, outputs)}")
    print(f"co2_ems: {co2_ems(inputs, outputs, 0.0)}")
    print(f"electricity_price_new: {electricity_price_new(inputs, outputs)}")
    print(f"fixed_invest: {fixed_invest(inputs, outputs)}")
    print(f"el_revenue: {el_revenue(inputs, outputs)}")
    print(f"hy_revenue: {hy_revenue(inputs, outputs)}")
```
