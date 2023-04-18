import geopandas as gpd

from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
def fill_hole(s: gpd.GeoSeries, /) -> gpd.GeoSeries:
    """
    Fill holes in Polygon.

    Returns
    -------
    GeoSeries

    See Also
    --------
    dtoolkit.geoaccessor.geoseries.fill_hole
    dtoolkit.geoaccessor.geoseries.has_hole
    dtoolkit.geoaccessor.geoseries.hole_counts
    dtoolkit.geoaccessor.geodataframe.fill_hole
    dtoolkit.geoaccessor.geodataframe.has_hole
    dtoolkit.geoaccessor.geodataframe.hole_counts

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import geopandas as gpd
    >>> from shapely import LineString, Point, Polygon
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
    >>> df.fill_hole()
    0    POLYGON ((0.00000 0.00000, 0.00000 5.00000, 5....
    1    POLYGON ((0.00000 0.00000, 2.00000 1.00000, 1....
    2    LINESTRING (0.00000 0.00000, 0.00000 5.00000, ...
    3                              POINT (0.00000 0.00000)
    dtype: geometry
    """

    return s.exterior.convex_hull.fillna(s)
