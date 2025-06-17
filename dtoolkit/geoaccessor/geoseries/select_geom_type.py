from __future__ import annotations

from typing import Literal

import geopandas as gpd
from pandas.util._decorators import doc

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
@doc(klass="GeoSeries")
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
    geom_type : {{"Point", "MultiPoint", "LineString", "LinearRing", \
"MultiLineString", "Polygon", "MultiPolygon", "GeometryCollection"}}
        Geometry type.

    complement : bool, default False
        If True, do operation reversely.

    Returns
    -------
    {klass}
        Return selected geometries.

    See Also
    --------
    geopandas.GeoSeries.geom_type
    dtoolkit.geoaccessor.geoseries.select_geom_type
    dtoolkit.geoaccessor.geodataframe.select_geom_type

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd
    >>> df = pd.DataFrame({{
    ...     "wkt": [
    ...         "POINT (1 1)",
    ...         "MULTIPOINT (1 1, 2 2)",
    ...         "LINESTRING (1 1, 2 2)",
    ...         "LINEARRING (0 0, 0 1, 1 1, 1 0, 0 0)",
    ...         "MULTILINESTRING ((1 1, 2 2), (3 3, 4 4))",
    ...         "POLYGON ((0 0, 0 1, 1 1, 1 0, 0 0))",
    ...         "MULTIPOLYGON (((0 0, 0 1, 1 1, 1 0, 0 0)))",
    ...         "GEOMETRYCOLLECTION (POINT (1 1), LINESTRING (1 1, 2 2))",
    ...     ],
    ... }}).from_wkt("wkt").drop(columns="wkt")
    >>> df
                                                geometry
    0                                        POINT (1 1)
    1                          MULTIPOINT ((1 1), (2 2))
    2                              LINESTRING (1 1, 2 2)
    3               LINEARRING (0 0, 0 1, 1 1, 1 0, 0 0)
    4           MULTILINESTRING ((1 1, 2 2), (3 3, 4 4))
    5                POLYGON ((0 0, 0 1, 1 1, 1 0, 0 0))
    6         MULTIPOLYGON (((0 0, 0 1, 1 1, 1 0, 0 0)))
    7  GEOMETRYCOLLECTION (POINT (1 1), LINESTRING (1...
    >>> df.select_geom_type("Point")
          geometry
    0  POINT (1 1)
    """

    return s[invert_or_not(s.geom_type == geom_type, invert=complement)]
