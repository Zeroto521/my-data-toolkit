import geopandas as gpd

from dtoolkit.accessor.series import invert_or_not
from dtoolkit.geoaccessor.geoseries.select_geom_type import GEOM_TYPE
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
def select_geom_type(
    df: gpd.GeoDataFrame,
    geom_type: GEOM_TYPE,
    /,
    complement: bool = False,
) -> gpd.GeoDataFrame:
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
    GeoDataFrame
        GeoDataFrame with selected geometries.

    See Also
    --------
    geopandas.GeoSeries.geom_type
    dtoolkit.geoaccessor.geoseries.select_geom_type

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd
    >>> df = pd.DataFrame({
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
    ... }).from_wkt("wkt").drop(columns="wkt")
    >>> df
                                                geometry
    0                            POINT (1.00000 1.00000)
    1      MULTIPOINT (1.00000 1.00000, 2.00000 2.00000)
    2      LINESTRING (1.00000 1.00000, 2.00000 2.00000)
    3  LINEARRING (0.00000 0.00000, 0.00000 1.00000, ...
    4  MULTILINESTRING ((1.00000 1.00000, 2.00000 2.0...
    5  POLYGON ((0.00000 0.00000, 0.00000 1.00000, 1....
    6  MULTIPOLYGON (((0.00000 0.00000, 0.00000 1.000...
    7  GEOMETRYCOLLECTION (POINT (1.00000 1.00000), L...
    >>> df.select_geom_type("Point")
                      geometry
    0  POINT (1.00000 1.00000)
    """

    return df[invert_or_not(df.geom_type == geom_type, invert=complement)]
