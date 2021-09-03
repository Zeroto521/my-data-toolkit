from __future__ import annotations

from warnings import warn

import geopandas as gpd
import pandas as pd
from more_itertools import collapse
from shapely.geometry import mapping
from shapely.geometry.base import BaseGeometry

from ._typing import CoordNumType
from ._typing import CoordType
from ._typing import NumericBaseList
from ._typing import NumericBaseType
from ._validation import check_geometry_type
from ._validation import check_geopandas_type
from ._validation import istype


def coords(df: gpd.GeoSeries | gpd.GeoDataFrame) -> pd.Series:
    check_geopandas_type(df)

    return df.geometry.apply(_coords)


def coords_numlist(df: gpd.GeoSeries | gpd.GeoDataFrame) -> pd.Series:
    check_geopandas_type(df)

    return df.geometry.apply(_coords_num)


def coords_num(df: gpd.GeoSeries | gpd.GeoDataFrame) -> pd.Series:
    res = coords_numlist(df)

    def sum_nums(nums: CoordNumType) -> NumericBaseType:
        if istype(nums, NumericBaseList):
            return nums

        return sum(collapse(nums, levels=1))

    return res.apply(sum_nums)


def _coords(geom: BaseGeometry) -> CoordType | tuple[CoordType]:
    check_geometry_type(geom)

    geom_dic = mapping(geom)
    return _get_coords(geom_dic)


def _get_coords(geom_dic: dict) -> CoordType | tuple[CoordType]:
    if geom_dic.get("type") != "GeometryCollection":
        return tuple(geom_dic.get("coordinates"))

    geoms = geom_dic.get("geometries")
    return (_get_coords(geom) for geom in geoms)


def _coords_num(geom: BaseGeometry) -> CoordNumType:
    check_geometry_type(geom)

    geom_dic = mapping(geom)
    return _get_coords_num(geom_dic)


def _get_coords_num(geom_dic: dict) -> CoordNumType:
    typ = geom_dic.get("type")
    coordinates = geom_dic.get("coordinates")

    if typ == "Point":
        return 1
    elif typ in ("LineString", "LinearRing", "MultiPoint"):
        return len(coordinates)
    elif typ in ("Polygon", "MultiLineString"):
        return tuple(len(c) for c in coordinates)
    elif typ == "MultiPolygon":
        return tuple(tuple(len(c) for c in g) for g in coordinates)
    elif typ == "GeometryCollection":
        geoms = geom_dic.get("geometries")
        return tuple(_get_coords_num(geom) for geom in geoms)

    warn("Unknown type %s" % typ, UserWarning)  # pragma: no cover
    return 0  # pragma: no cover
