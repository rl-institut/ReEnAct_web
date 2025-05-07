from reenact.reenact import datapackage

TEST_OEMOF_SCENARIO = "tabular_es5"


def test_potentials():
    potentials = datapackage.get_potentials(TEST_OEMOF_SCENARIO)
    assert len(potentials) == 6  # noqa: PLR2004


def test_full_load_hours():
    full_load_hours = datapackage.get_full_load_hours(TEST_OEMOF_SCENARIO)
    assert len(full_load_hours) == 8  # noqa: PLR2004
