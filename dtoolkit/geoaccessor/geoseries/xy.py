import geopandas as gpd
import pandas as pd

from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
def xy(s: gpd.GeoSeries, /, reverse: bool = False) -> pd.Series:
    """
    Return the x and y location of Point geometries in a GeoSeries.

    Parameters
    ----------
    reverse : bool, default False
        If True, return (y, x) instead.

    Returns
    -------
    Series
        tuple of coordinate.

    See Also
    --------
    geopandas.GeoSeries.x
    geopandas.GeoSeries.y

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import geopandas as gpd
    >>> from shapely.geometry import Point
    >>> s = gpd.GeoSeries([Point(0, 1), Point(0, 2), Point(0, 3)])
    >>> s
    0    POINT (0.00000 1.00000)
    1    POINT (0.00000 2.00000)
    2    POINT (0.00000 3.00000)
    dtype: geometry
    >>> s.xy()
    0    (0.0, 1.0)
    1    (0.0, 2.0)
    2    (0.0, 3.0)
    dtype: object

    Set ``reverse=True`` to return (y, x).

    >>> s.xy(True)
    0    (1.0, 0.0)
    1    (2.0, 0.0)
    2    (3.0, 0.0)
    dtype: object
    """

    coordinates = (s.y, s.x) if reverse else (s.x, s.y)
    return pd.concat(coordinates, axis=1).apply(tuple, axis=1)
