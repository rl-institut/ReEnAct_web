import os
from oemof.tabular.datapackage import building

building.infer_metadata(
    package_name="my-datapackage",
    foreign_keys={
        "bus": [
            "dispatchable",
            "excess",
            "export",
            "import",
            "load",
            "storage",
            "volatile",
        ],
        "profile": ["load", "volatile"],
        "efficiency": ["decentral_hp"],
        "from_to_bus": ["conversion", "decentral_hp", "link"],
        "chp": ["backpressure", "extraction"],
        "marginal_cost": ["import", "export"],
    },
    path=os.path.dirname(os.path.dirname(__file__)),
)
