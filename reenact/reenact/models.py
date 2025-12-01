"""Models for map-based layers in the reenact app."""

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
    """Static layer of agricultural areas."""

    data_file = "agricultural_area"
    layer = "agricultural_area"


class BirdProtectionArea(StaticRegionModel):
    """Static layer of bird protection areas."""

    data_file = "bird_protection_area"
    layer = "bird_protection_area"


class CadastralParcels(StaticRegionModel):
    """Static layer of cadastral parcels."""

    data_file = "cadastral_parcels"
    layer = "cadastral_parcels"


class FaunaFloraHabitatArea(StaticRegionModel):
    """Static layer of Fauna-Flora-Habitat (FFH) areas."""

    data_file = "fauna_flora_habitat"
    layer = "fauna_flora_habitat"


class Forest(StaticRegionModel):
    """Static layer of forest areas."""

    data_file = "forest"
    layer = "forest"


class ForestProtected(StaticRegionModel):
    """Static layer of protected forest areas."""

    data_file = "forest_protected"
    layer = "forest_protected"


class GeneratorBiomass(StaticRegionModel):
    """Point layer of biomass generators."""

    geom = models.PointField(srid=4326)
    data_file = "generator_biomass"
    layer = "generator_biomass"
    mapping = {"geom": "POINT"}


class GeneratorPvGround(StaticRegionModel):
    """Point layer of ground-mounted PV generators."""

    geom = models.PointField(srid=4326)
    data_file = "generator_pv_ground"
    layer = "generator_pv_ground"
    mapping = {"geom": "POINT"}


class GeneratorPvRoof(StaticRegionModel):
    """Point layer of rooftop PV generators."""

    geom = models.PointField(srid=4326)
    data_file = "generator_pv_roof"
    layer = "generator_pv_roof"
    mapping = {"geom": "POINT"}


class GeneratorWind15a(StaticRegionModel):
    """Point layer of wind generators (15a)."""

    geom = models.PointField(srid=4326)
    data_file = "generator_wind_15a"
    layer = "generator_wind_15a"
    mapping = {"geom": "POINT"}


class GeneratorWind25a(StaticRegionModel):
    """Point layer of wind generators (25a)."""

    geom = models.PointField(srid=4326)
    data_file = "generator_wind_25a"
    layer = "generator_wind_25a"
    mapping = {"geom": "POINT"}


class GeneratorWind(StaticRegionModel):
    """Point layer of wind generators."""

    geom = models.PointField(srid=4326)
    data_file = "generator_wind"
    layer = "generator_wind"
    mapping = {"geom": "POINT"}


class Grassland(StaticRegionModel):
    """Static layer of grassland areas."""

    data_file = "grassland"
    layer = "grassland"


class LandscapeProtectionArea(StaticRegionModel):
    """Static layer of landscape protection areas."""

    data_file = "landscape_protection_area"
    layer = "landscape_protection_area"


class Meadow(StaticRegionModel):
    """Static layer of meadows."""

    data_file = "meadow"
    layer = "meadow"


class NaturalParks(StaticRegionModel):
    """Static layer of natural parks."""

    data_file = "natural_parks"
    layer = "natural_parks"


class NatureConservationArea(StaticRegionModel):
    """Static layer of nature conservation areas."""

    data_file = "nature_conservation_area"
    layer = "nature_conservation_area"


class OrganicSoils(StaticRegionModel):
    """Static layer of organic soils (peat) areas."""

    data_file = "organic_soils"
    layer = "organic_soils"


class PotentialareaPaludicultureKlasse1(StaticRegionModel):
    """Potential areas for paludiculture class 1."""

    data_file = "potentialarea_paludiculture_Klasse_1"
    layer = "potentialarea_paludiculture_Klasse_1"


class PotentialareaPaludicultureKlasse2(StaticRegionModel):
    """Potential areas for paludiculture class 2."""

    data_file = "potentialarea_paludiculture_Klasse_2"
    layer = "potentialarea_paludiculture_Klasse_2"


class PotentialareaPaludicultureKlasse3(StaticRegionModel):
    """Potential areas for paludiculture class 3."""

    data_file = "potentialarea_paludiculture_Klasse_3"
    layer = "potentialarea_paludiculture_Klasse_3"


class PotentialareaPaludicultureMoorOhneFeldblock(StaticRegionModel):
    """Potential paludiculture areas on moor (without field block)."""

    data_file = "potentialarea_paludiculture_Moor_ohne_Feldblock"
    layer = "potentialarea_paludiculture_Moor_ohne_Feldblock"


class PotentialareaPaludicultureNichtEignung(StaticRegionModel):
    """Areas not suitable for paludiculture."""

    data_file = "potentialarea_paludiculture_Nicht-Eignung"
    layer = "potentialarea_paludiculture_Nicht-Eignung"


class PotentialareaPvGround(StaticRegionModel):
    """Potential areas for ground-mounted PV."""

    data_file = "potentialarea_pv_ground"
    layer = "potentialarea_pv_ground"


class PotentialareaPvRoof(StaticRegionModel):
    """Potential areas for rooftop PV."""

    data_file = "potentialarea_pv_roof"
    layer = "potentialarea_pv_roof"


class PotentialareaWind1000m(StaticRegionModel):
    """Potential wind areas (1000 m buffer)."""

    data_file = "potentialarea_wind_1000m"
    layer = "potentialarea_wind_1000m"


class PotentialareaWind400m(StaticRegionModel):
    """Potential wind areas (400 m buffer)."""

    data_file = "potentialarea_wind_400m"
    layer = "potentialarea_wind_400m"


class PotentialareaWind600m(StaticRegionModel):
    """Potential wind areas (600 m buffer)."""

    data_file = "potentialarea_wind_600m"
    layer = "potentialarea_wind_600m"


class PotentialareaWind800m(StaticRegionModel):
    """Potential wind areas (800 m buffer)."""

    data_file = "potentialarea_wind_800m"
    layer = "potentialarea_wind_800m"


class PotentialareaWindRpg2024Draft(StaticRegionModel):
    """Potential wind areas (RPG 2024 draft)."""

    data_file = "potentialarea_wind_rpg_2024_draft"
    layer = "potentialarea_wind_rpg_2024_draft"


class PowerGrid(StaticRegionModel):
    """Multi-line layer of power grid segments."""

    geom = models.MultiLineStringField(srid=4326)
    data_file = "power_grid"
    layer = "power_grid"
    mapping = {"geom": "MULTILINESTRING"}


class ProtectedLandscapeParts(StaticRegionModel):
    """Static layer of protected parts of the landscape."""

    data_file = "protected_landscape_parts"
    layer = "protected_landscape_parts"


class RoofGeneratorPvRoof(StaticRegionModel):
    """Static layer for roof geometry used for PV potential."""

    data_file = "roof_generator_pv_roof"
    layer = "roof_generator_pv_roof"


class WaterAndDrinkingWaterProtectionArea(StaticRegionModel):
    """Static layer of water and drinking water protection areas."""

    data_file = "water_and_drinking_water_protection_area"
    layer = "water_and_drinking_water_protection_area"
