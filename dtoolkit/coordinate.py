from __future__ import annotations

from typing import Tuple
from warnings import warn

import geopandas as gpd
from shapely.geometry import mapping
from shapely.geometry.base import BaseGeometry

from ._checking import check_geometry_type
from ._typing import CoordLenType, CoordType


def coords(
    df: gpd.GeoSeries | gpd.GeoDataFrame,
) -> Tuple[CoordType] | Tuple[Tuple[CoordType]]:

    return (_coords(g) for g in df.geometry)


def coords_num(
    df: gpd.GeoSeries | gpd.GeoDataFrame,
) -> Tuple[CoordLenType] | Tuple[Tuple[CoordLenType]]:

    return (_coords_num(g) for g in df.geometry)


def _coords(geom: BaseGeometry) -> CoordType | Tuple[CoordType]:
    check_geometry_type(geom)

    geom_dic = mapping(geom)
    return _get_coords(geom_dic)


def _get_coords(geom_dic: dict) -> CoordType | Tuple[CoordType]:
    if geom_dic.get("type") != "GeometryCollection":
        return geom_dic.get("coordinates")

    geoms = geom_dic.get("geometries")
    return (_get_coords(geom) for geom in geoms)


def _coords_num(geom: BaseGeometry) -> CoordLenType:
    check_geometry_type(geom)

    geom_dic = mapping(geom)
    return _get_coords_num(geom_dic)


def _get_coords_num(geom_dic: dict) -> CoordLenType:
    typ = geom_dic.get("type")
    coordinates = geom_dic.get("coordinates")

    if typ == "Point":
        return 1
    elif typ in ("LineString", "LinearRing"):
        return len(coordinates)
    elif typ in ("Polygon", "MultiLineString"):
        return (len(c) for c in coordinates)
    elif typ == "MultiPolygon":
        return ((len(c) for c in g) for g in coordinates)
    elif typ == "GeometryCollection":
        geoms = geom_dic.get("geometries")
        return (_get_coords_num(geom) for geom in geoms)
    else:
        warn("Unknown type %s" % typ, UserWarning)
        return 0
