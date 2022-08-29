import geopandas as gpd
import pandas as pd

from dtoolkit.geoaccessor.geoseries.hole_counts import hole_counts
from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
def has_hole(s: gpd.GeoSeries, /) -> pd.Series:
    """
    Check if each Polygon geometries have holes.

    Except for Polygon and MultiPolygon, other geometries will return ``False``.

    Returns
    -------
    Series

    See Also
    --------
    geopandas.GeoSeries.convex_hull : Drop holes in Polygon and MultiPolygon.
    dtoolkit.geoaccessor.geoseries.has_hole
    dtoolkit.geoaccessor.geoseries.hole_counts
    dtoolkit.geoaccessor.geodataframe.has_hole
    dtoolkit.geoaccessor.geodataframe.hole_counts

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import geopandas as gpd
    >>> from shapely.geometry import LineString, Point, Polygon
    >>> df = gpd.GeoDataFrame(
    ...     geometry=[
    ...         Polygon(
    ...             [(0, 0), (0, 5), (5, 5), (5, 0)],
    ...             [[(1, 1), (2, 1), (1, 2)], [(1, 4), (2, 4), (2, 3)]],
    ...         ),
    ...         Polygon([(1, 0), (2, 1), (0, 0)]),
    ...         LineString([(0, 0), (0, 5), (5, 5), (5, 0)]),
    ...         Point(0, 0),
    ...     ]
    ... )
    >>> df
                                                geometry
    0  POLYGON ((0.00000 0.00000, 0.00000 5.00000, 5....
    1  POLYGON ((1.00000 0.00000, 2.00000 1.00000, 0....
    2  LINESTRING (0.00000 0.00000, 0.00000 5.00000, ...
    3                            POINT (0.00000 0.00000)
    >>> df.has_hole()
    0     True
    1    False
    2    False
    3    False
    dtype: bool
    """

    return hole_counts(s) >= 1
