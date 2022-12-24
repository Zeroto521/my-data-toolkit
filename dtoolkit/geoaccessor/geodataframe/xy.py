from __future__ import annotations

from typing import Hashable

import geopandas as gpd
import pandas as pd

from dtoolkit._typing import SeriesOrFrame
from dtoolkit.geoaccessor.geodataframe.drop_geometry import drop_geometry
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
        If True, only return the new generated coordinates.

    name : Hashable or a tuple of Hashable, default ('x', 'y')
        If ``frame=True``, the column names of the returned DataFrame,
        else the name of the returned Series.

    Returns
    -------
    Series, DataFrame or GeoDataFrame
        - If ``drop=Fasle``, return a GeoDataFrame with the new generated coordinates.

        - If ``drop=True`` and ``frame=True``, return a DataFrame with x and y two
          columns.

        - If ``drop=True`` and ``frame=False``, return a DataFrame with tuple of
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
    >>> from shapely import Point
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
    0 0.0  1.0
    1 0.0  2.0
    2 0.0  3.0

    Keep other columns.

    >>> df.xy(drop=False)
        x    y                 geometry  label
    0 0.0  1.0  POINT (0.00000 1.00000)      a
    1 0.0  2.0  POINT (0.00000 2.00000)      b
    2 0.0  3.0  POINT (0.00000 3.00000)      c
    """

    coord = s_xy(df.geometry, reverse=reverse, frame=frame, drop=drop, name=name)
    return coord if drop else pd.concat((coord, drop_geometry(df)), axis=1)
