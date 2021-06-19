from __future__ import annotations

from typing import List
from warnings import warn

import geopandas as gpd
from shapely.geometry import mapping
from shapely.geometry.base import BaseGeometry

from ._checking import check_geometry_type
from ._typing import CoordLenType, CoordType


def coords(df: gpd.GeoSeries | gpd.GeoDataFrame) -> List[CoordType]:
    return [_coords(g) for g in df.geometry]


def coords_num(df: gpd.GeoSeries | gpd.GeoDataFrame) -> List[CoordLenType]:
    return [_coords_num(g) for g in df.geometry]


def _coords(geom: BaseGeometry) -> CoordType:
    check_geometry_type(geom)

    geom_dic = mapping(geom)
    return geom_dic["coordinates"]


def _coords_num(geom: BaseGeometry) -> CoordLenType:
    check_geometry_type(geom)

    typ, coordinates = mapping(geom)

    if typ == "Point":
        return 1
    elif typ in ("LineString", "LinearRing"):
        return len(coordinates)
    elif typ in ("Polygon", "MultiLineString"):
        return (len(c) for c in coordinates)
    elif typ == "MultiPolygon":
        return ((len(c) for c in g) for g in coordinates)
    else:
        warn("Unknown type %s" % typ, UserWarning)
        return 0

