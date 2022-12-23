from __future__ import annotations

from typing import Literal

import geopandas as gpd

from dtoolkit.accessor.series import invert_or_not
from dtoolkit.geoaccessor.register import register_geoseries_method


GEOM_TYPE = Literal[
    "Point",
    "MultiPoint",
    "LineString",
    "LinearRing",
    "MultiLineString",
    "Polygon",
    "MultiPolygon",
    "GeometryCollection",
]


@register_geoseries_method
def select_geom_type(
    s: gpd.GeoSeries,
    geom_type: GEOM_TYPE,
    /,
    complement: bool = False,
) -> gpd.GeoSeires:
    """
    Select geometries by geometry type.

    Parameters
    ----------
    geom_type : {"Point", "MultiPoint", "LineString", "LinearRing", "MultiLineString", \
"Polygon", "MultiPolygon", "GeometryCollection"}
        Geometry type.

    complement : bool, default False
        If True, do operation reversely.

    Returns
    -------
    GeoSeries
        GeoSeries with selected geometries.

    See Also
    --------
    geopandas.GeoSeries.geom_type
    dtoolkit.geoaccessor.geodataframe.select_geom_type

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd
    >>> s = pd.Series(
    ...     [
    ...         "POINT (1 1)",
    ...         "MULTIPOINT (1 1, 2 2)",
    ...         "LINESTRING (1 1, 2 2)",
    ...         "LINEARRING (0 0, 0 1, 1 1, 1 0, 0 0)",
    ...         "MULTILINESTRING ((1 1, 2 2), (3 3, 4 4))",
    ...         "POLYGON ((0 0, 0 1, 1 1, 1 0, 0 0))",
    ...         "MULTIPOLYGON (((0 0, 0 1, 1 1, 1 0, 0 0)))",
    ...         "GEOMETRYCOLLECTION (POINT (1 1), LINESTRING (1 1, 2 2))",
    ...     ],
    ...     name="wkt",
    ... ).from_wkt("wkt").geometry
    >>> s
    0                                  POINT (1.000 1.000)
    1                MULTIPOINT (1.000 1.000, 2.000 2.000)
    2                LINESTRING (1.000 1.000, 2.000 2.000)
    3    LINEARRING (0.000 0.000, 0.000 1.000, 1.000 1....
    4    MULTILINESTRING ((1.000 1.000, 2.000 2.000), (...
    5    POLYGON ((0.000 0.000, 0.000 1.000, 1.000 1.00...
    6    MULTIPOLYGON (((0.000 0.000, 0.000 1.000, 1.00...
    7    GEOMETRYCOLLECTION (POINT (1.000 1.000), LINES...
    Name: geometry, dtype: geometry
    >>> s.select_geom_type("Point")
    0    POINT (1.000 1.000)
    Name: geometry, dtype: geometry
    """

    return s[invert_or_not(s.geom_type == geom_type, invert=complement)]
