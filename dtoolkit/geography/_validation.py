from __future__ import annotations

from shapely.geometry.base import BaseGeometry

from dtoolkit._typing import get_args
from dtoolkit.geography._typing import GeoSeriesOrGeoFrame


def check_geopandas_type(df: GeoSeriesOrGeoFrame):
    if not isinstance(df, get_args(GeoSeriesOrGeoFrame)):
        raise TypeError(f"{df} must be GeoSeries or GeoDataFrame.")


def check_geometry_type(geom: BaseGeometry):
    if not isinstance(geom, BaseGeometry):
        raise TypeError(f"{geom} must be Geometry.")
