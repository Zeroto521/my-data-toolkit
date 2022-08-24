import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.accessor.series import len
from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
@doc(alias="s")
def hole_counts(s: gpd.GeoSeries, /) -> pd.Series:
    """
    Return the number of holes in each Polygon geometries.

    A sugar syntax for ``{alias}.interiors.apply(len)``.

    Returns
    -------
    Series
        Except for Polygon and MultiPolygon, others will get ``NaN``.

    See Also
    --------
    geopandas.GeoSeries.interiors : Inner boundary.
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
    >>> df.hole_counts()
    0    2.0
    1    0.0
    2    NaN
    3    NaN
    dtype: float64
    """

    return len(s.interiors)
