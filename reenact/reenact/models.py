from django.contrib.gis.db import models
from .managers import RegionMVTManager, StaticMVTManager, LabelMVTManager


class Municipality(models.Model):
    """Model for region level municipality."""

    geom = models.MultiPolygonField(srid=4326)
    name = models.CharField(max_length=50, unique=True)

    objects = models.Manager()
    vector_tiles = RegionMVTManager(columns=["id", "name", "bbox"])
    label_tiles = LabelMVTManager(geo_col="geom_label", columns=["id", "name"])

    data_file = "municipalities"
    layer = "municipalities"
    mapping = {"id": "id", "geom": "MULTIPOLYGON", "name": "GEN"}

    class Meta:
        verbose_name = "Municipality"
        verbose_name_plural = "Municipalities"

    def __str__(self) -> str:
        """Return string representation of the model."""
        return self.name


class StaticRegionModel(models.Model):
    """Base class for static region models."""

    geom = models.MultiPolygonField(srid=4326)

    objects = models.Manager()
    vector_tiles = StaticMVTManager(columns=[])

    mapping = {"geom": "MULTIPOLYGON"}

    class Meta:
        abstract = True


class AgriculturalArea(StaticRegionModel):
    data_file = "agricultural_area"
    layer = "agricultural_area"


class BirdProtectionArea(StaticRegionModel):
    data_file = "bird_protection_area"
    layer = "bird_protection_area"


class CadastralParcels(StaticRegionModel):
    data_file = "cadastral_parcels"
    layer = "cadastral_parcels"


class FaunaFloraHabitatArea(StaticRegionModel):
    data_file = "fauna_flora_habitat"
    layer = "fauna_flora_habitat"


class Forest(StaticRegionModel):
    data_file = "forest"
    layer = "forest"


class ForestProtected(StaticRegionModel):
    data_file = "forest_protected"
    layer = "forest_protected"


class GeneratorBiomass(StaticRegionModel):
    geom = models.PointField(srid=4326)
    data_file = "generator_biomass"
    layer = "generator_biomass"
    mapping = {"geom": "POINT"}


class GeneratorPvGround(StaticRegionModel):
    geom = models.PointField(srid=4326)
    data_file = "generator_pv_ground"
    layer = "generator_pv_ground"
    mapping = {"geom": "POINT"}


class GeneratorPvRoof(StaticRegionModel):
    geom = models.PointField(srid=4326)
    data_file = "generator_pv_roof"
    layer = "generator_pv_roof"
    mapping = {"geom": "POINT"}


class GeneratorWind15a(StaticRegionModel):
    geom = models.PointField(srid=4326)
    data_file = "generator_wind_15a"
    layer = "generator_wind_15a"
    mapping = {"geom": "POINT"}


class GeneratorWind25a(StaticRegionModel):
    geom = models.PointField(srid=4326)
    data_file = "generator_wind_25a"
    layer = "generator_wind_25a"
    mapping = {"geom": "POINT"}


class GeneratorWind(StaticRegionModel):
    geom = models.PointField(srid=4326)
    data_file = "generator_wind"
    layer = "generator_wind"
    mapping = {"geom": "POINT"}


class Grassland(StaticRegionModel):
    data_file = "grassland"
    layer = "grassland"


class LandscapeProtectionArea(StaticRegionModel):
    data_file = "landscape_protection_area"
    layer = "landscape_protection_area"


class Meadow(StaticRegionModel):
    data_file = "meadow"
    layer = "meadow"


class NaturalParks(StaticRegionModel):
    data_file = "natural_parks"
    layer = "natural_parks"


class NatureConservationArea(StaticRegionModel):
    data_file = "nature_conservation_area"
    layer = "nature_conservation_area"


class OrganicSoils(StaticRegionModel):
    data_file = "organic_soils"
    layer = "organic_soils"


class PotentialareaPaludicultureKlasse1(StaticRegionModel):
    data_file = "potentialarea_paludiculture_Klasse_1"
    layer = "potentialarea_paludiculture_Klasse_1"


class PotentialareaPaludicultureKlasse2(StaticRegionModel):
    data_file = "potentialarea_paludiculture_Klasse_2"
    layer = "potentialarea_paludiculture_Klasse_2"


class PotentialareaPaludicultureKlasse3(StaticRegionModel):
    data_file = "potentialarea_paludiculture_Klasse_3"
    layer = "potentialarea_paludiculture_Klasse_3"


class PotentialareaPaludicultureMoorOhneFeldblock(StaticRegionModel):
    data_file = "potentialarea_paludiculture_Moor_ohne_Feldblock"
    layer = "potentialarea_paludiculture_Moor_ohne_Feldblock"


class PotentialareaPaludicultureNichtEignung(StaticRegionModel):
    data_file = "potentialarea_paludiculture_Nicht-Eignung"
    layer = "potentialarea_paludiculture_Nicht-Eignung"


class PotentialareaPvGround(StaticRegionModel):
    data_file = "potentialarea_pv_ground"
    layer = "potentialarea_pv_ground"


class PotentialareaPvRoof(StaticRegionModel):
    data_file = "potentialarea_pv_roof"
    layer = "potentialarea_pv_roof"


class PotentialareaWind1000m(StaticRegionModel):
    data_file = "potentialarea_wind_1000m"
    layer = "potentialarea_wind_1000m"


class PotentialareaWind400m(StaticRegionModel):
    data_file = "potentialarea_wind_400m"
    layer = "potentialarea_wind_400m"


class PotentialareaWind600m(StaticRegionModel):
    data_file = "potentialarea_wind_600m"
    layer = "potentialarea_wind_600m"


class PotentialareaWind800m(StaticRegionModel):
    data_file = "potentialarea_wind_800m"
    layer = "potentialarea_wind_800m"


class PotentialareaWindRpg2024Draft(StaticRegionModel):
    data_file = "potentialarea_wind_rpg_2024_draft"
    layer = "potentialarea_wind_rpg_2024_draft"


class PowerGrid(StaticRegionModel):
    geom = models.MultiLineStringField(srid=4326)
    data_file = "power_grid"
    layer = "power_grid"
    mapping = {"geom": "MULTILINESTRING"}


class ProtectedLandscapeParts(StaticRegionModel):
    data_file = "protected_landscape_parts"
    layer = "protected_landscape_parts"


class RoofGeneratorPvRoof(StaticRegionModel):
    data_file = "roof_generator_pv_roof"
    layer = "roof_generator_pv_roof"


class WaterAndDrinkingWaterProtectionArea(StaticRegionModel):
    data_file = "water_and_drinking_water_protection_area"
    layer = "water_and_drinking_water_protection_area"
