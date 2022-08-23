import geopandas as gpd
import pandas as pd
import pygeos
from pandas.util._decorators import doc

from dtoolkit.accessor.series import set_unique_index
from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
@doc(klass="GeoSeries", alias="s")
def drop_hole(s: gpd.GeoSeries, /) -> gpd.GeoSeries:
    """
    Drop holes from Polygon geometries.

    A sugar syntax for ``{alias}.exterior.convex_hull``.

    Returns
    -------
    {klass}

    See Also
    --------
    geopandas.GeoSeries.exterior
    dtoolkit.geoaccessor.geoseries.drop_hole
    dtoolkit.geoaccessor.geodataframe.drop_hole

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
    >>> df.drop_hole()
    0    POLYGON ((0.00000 0.00000, 0.00000 5.00000, 5....
    1    POLYGON ((0.00000 0.00000, 2.00000 1.00000, 1....
    2    LINESTRING (0.00000 0.00000, 0.00000 5.00000, ...
    3                              POINT (0.00000 0.00000)
    dtype: geometry
    """

    result = s.exterior.convex_hull

    try:
        return result.fillna(s)
    except NotImplementedError:
        # Still to geopandas 0.11, only supports filling with a single scalar geometry
        s_index = s.index
        s = set_unique_index(s)
        result = result.reset_index(drop=True)

        # use `ndarray` instead of Series to slice
        mask = result.isna().to_numpy()
        return (
            pd.concat(
                (
                    result[~mask],
                    s[mask],
                )
            )
            .sort_index()
            .set_axis(s_index)
        )
