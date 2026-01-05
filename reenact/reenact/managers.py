"""Module holds module managers for MVT layers in mapengine."""

from django.contrib.gis.db import models
from django_mapengine.managers import MVTManager


class RegionMVTManager(MVTManager):
    """Manager which adds bbox to layer features to better show regions in the frontend."""

    def get_queryset(self) -> models.QuerySet:
        """Annotate bbox to queryset."""
        return (
            super()
            .get_queryset()
            .annotate(
                bbox=models.functions.AsGeoJSON(models.functions.Envelope("geom")),
            )
        )


class StaticMVTManager(MVTManager):
    """Manager which does nothing?."""

    # pylint: disable=R0913
    def _filter_query(
        self,
        query: models.QuerySet,
        x: int,
        y: int,
        z: int,
        filters: dict,
    ) -> models.QuerySet:
        query = super()._filter_query(query, x, y, z, filters)
        return query


class LabelMVTManager(MVTManager):
    """Manager which adds centroid of geom to place label."""

    def get_queryset(self) -> models.QuerySet:
        """Return queryset with added centroid."""
        return (
            super()
            .get_queryset()
            .annotate(geom_label=models.functions.Centroid("geom"))
        )
