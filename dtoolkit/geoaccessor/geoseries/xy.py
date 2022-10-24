from typing import Hashable

import geopandas as gpd
import pandas as pd

from dtoolkit._typing import SeriesOrFrame
from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
def xy(
    s: gpd.GeoSeries,
    /,
    reverse: bool = False,
    frame: bool = False,
    x: Hashable = "x",
    y: Hashable = "y",
) -> SeriesOrFrame:
    """
    Return the x and y location of Point geometries in a GeoSeries.

    Parameters
    ----------
    reverse : bool, default False
        If True, return (y, x) instead.

    frame : bool, default False
        If True, return a DataFrame instead of a Series.

    x : str, default 'x'
        Name of the x column if frame=True.

    y : str, default 'y'
        Name of the y column if frame=True.

    Returns
    -------
    Series or DataFrame
        If frame=False, a Series with tuple of coordinate. else, a DataFrame with
        x and y two columns.

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

    Get the x and y coordinates of each point as a tuple.

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

    Set ``frame=True`` to return a DataFrame with x and y columns.

    >>> s.xy(frame=True)
         x    y
    0  0.0  1.0
    1  0.0  2.0
    2  0.0  3.0
    """

    coords = pd.concat((s.x.rename(x), s.y.rename(y)), axis=1)

    if reverse:
        coords = coords.iloc[:, ::-1]

    return coords if frame else coords.apply(tuple, axis=1)
