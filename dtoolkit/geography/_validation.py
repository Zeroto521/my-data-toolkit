from __future__ import annotations

from typing import Any

import geopandas as gpd
from shapely.geometry.base import BaseGeometry


def check_geopandas_type(df: gpd.GeoSeries | gpd.GeoDataFrame):
    if not isinstance(df, (gpd.GeoSeries, gpd.GeoDataFrame)):
        raise TypeError(f"{df} must be GeoSeries or GeoDataFrame.")


def check_geometry_type(geom: BaseGeometry):
    if not isinstance(geom, BaseGeometry):
        raise TypeError(f"{geom} must be Geometry.")


def istype(var: Any, types: type | list[type] | tuple[type]) -> bool:
    types: tuple[type] = containerize(types, tuple)

    return isinstance(var, types)


def containerize(var: Any, finaltype=list) -> list[Any] | tuple[Any]:
    if not isinstance(var, (list, tuple)):
        var = [var]

    return finaltype(var)
