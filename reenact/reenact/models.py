from django.contrib.gis.db import models
from .managers import RegionMVTManager, StaticMVTManager, LabelMVTManager


class Municipality(models.Model):
    """Model for region level municipality."""

    geom = models.MultiPolygonField(srid=4326)
    name = models.CharField(max_length=50, unique=True)
    area = models.FloatField()

    objects = models.Manager()
    vector_tiles = RegionMVTManager(columns=["id", "name", "bbox"])
    label_tiles = LabelMVTManager(geo_col="geom_label", columns=["id", "name"])

    data_file = "bkg_vg_250_muns"
    layer = "bkg_vg_250_muns"
    mapping = {"id": "id", "geom": "MULTIPOLYGON", "name": "name", "area": "area_km2"}

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


class FaunaFloraHabitat(StaticRegionModel):
    data_file = "fauna_flora_habitat_region"
    layer = "fauna_flora_habitat_region"
