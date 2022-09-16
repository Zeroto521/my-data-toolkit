import geopandas as gpd
import pandas as pd

from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
def xy(s: gpd.GeoSeries, /) -> pd.Series:
    """
    Return the x and y location of Point geometries in a GeoSeries.

    Returns
    -------
    Series
        tuple of x and y coordinates.

    See Also
    --------
    geopandas.GeoSeries.x
    geopandas.GeoSeries.y

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import geopandas as gpd
    >>> from shapely.geometry import Point
    >>> s = gpd.GeoSeries([Point(1, 1), Point(2, 2), Point(3, 3)])
    >>> s
    0    POINT (1.00000 1.00000)
    1    POINT (2.00000 2.00000)
    2    POINT (3.00000 3.00000)
    dtype: geometry
    >>> s.xy()
    0    (1.0, 1.0)
    1    (2.0, 2.0)
    2    (3.0, 3.0)
    dtype: object
    """

    return pd.concat((s.x, s.y), axis=1).apply(tuple, axis=1)
