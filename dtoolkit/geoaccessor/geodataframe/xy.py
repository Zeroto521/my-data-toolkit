from __future__ import annotations

from typing import Hashable

import geopandas as gpd
import pandas as pd

from dtoolkit._typing import SeriesOrFrame
from dtoolkit.geoaccessor.geoseries import xy as s_xy
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
def xy(
    df: gpd.GeoDataFrame,
    /,
    reverse: bool = False,
    frame: bool = True,
    drop: bool = True,
    name: Hashable | tuple[Hashable, Hashable] = ("x", "y"),
) -> SeriesOrFrame | gpd.GeoDataFrame:
    """
    Return the x and y location of Point geometries in a GeoDataFrame.

    Parameters
    ----------
    reverse : bool, default False
        If True, return (y, x) instead.

    frame : bool, default True
        If True, return a DataFrame.

    drop : bool, default True
        If True, drop the original geometry column.

    name : Hashable or a tuple of Hashable, default ('x', 'y')
        If ``frame=True``, the column names of the returned DataFrame,
        else the name of the returned Series.

    Returns
    -------
    Series, DataFrame, or GeoDataFrame
        - If ``drop=Fasle``, return a GeoDataFrame.

        - If ``drop=True`` and ``frame=True``, return a DataFrame with x and y two
          columns.

        - IF ``drop=True`` and ``frame=False``, return a Series with tuple of
          coordinate.

    See Also
    --------
    geopandas.GeoSeries.x
    geopandas.GeoSeries.y
    dtoolkit.geoaccessor.geoseries.xy

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import geopandas as gpd
    >>> from shapely.geometry import Point
    >>> df = gpd.GeoDataFrame({
    ...     "label": ["a", "b", "c"],
    ...     "geometry": [Point(0, 1), Point(0, 2), Point(0, 3)],
    ... })
    >>> df
      label                 geometry
    0     a  POINT (0.00000 1.00000)
    1     b  POINT (0.00000 2.00000)
    2     c  POINT (0.00000 3.00000)

    Get the x and y coordinates of each point as a tuple.

    >>> df.xy(frame=False, name=None)
    0    (0.0, 1.0)
    1    (0.0, 2.0)
    2    (0.0, 3.0)
    dtype: object

    Set ``reverse=True`` to return (y, x).

    >>> df.xy(reverse=True, frame=False, name=None)
    0    (1.0, 0.0)
    1    (2.0, 0.0)
    2    (3.0, 0.0)
    dtype: object

    Set ``frame=True`` to return a DataFrame with x and y columns.

    >>> df.xy()
         x    y
    0  0.0  1.0
    1  0.0  2.0
    2  0.0  3.0

    Keep the original geometry column.

    >>> df.xy(drop=False)
      label                 geometry    x    y
    0     a  POINT (0.00000 1.00000)  0.0  1.0
    1     b  POINT (0.00000 2.00000)  0.0  2.0
    2     c  POINT (0.00000 3.00000)  0.0  3.0
    """

    coords = s_xy(df.geometry, reverse=reverse, frame=frame, name=name)
    return coords if drop else pd.concat((df, coords), axis=1)
