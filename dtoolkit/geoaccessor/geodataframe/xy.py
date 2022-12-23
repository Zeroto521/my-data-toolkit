from __future__ import annotations

from typing import Hashable

import geopandas as gpd
import pandas as pd

from dtoolkit.geoaccessor.geoseries import xy as s_xy
from dtoolkit.geoaccessor.register import register_geodataframe_method
from dtoolkit.util._decorator import warning


@register_geodataframe_method
@warning(
    "The keyword argument 'drop' is deprecated, please use "
    "'.drop_geometry' method instead. (Warning added DToolKit 0.0.20)",
    category=DeprecationWarning,
    stacklevel=3,
)
def xy(
    df: gpd.GeoDataFrame,
    /,
    reverse: bool = False,
    frame: bool = True,
    name: Hashable | tuple[Hashable, Hashable] = ("x", "y"),
) -> gpd.GeoDataFrame:
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

        .. deprecated:: 0.0.20
            If you want to drop geometry column, please use
            :meth:`~dtoolkit.geoaccessor.geodataframe.drop_geometry` method instead.

    name : Hashable or a tuple of Hashable, default ('x', 'y')
        If ``frame=True``, the column names of the returned DataFrame,
        else the name of the returned Series.

    Returns
    -------
    GeoDataFrame

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

    Set ``frame=True`` to return a GeoDataFrame with x and y columns.

    >>> df.xy()
      label                 geometry    x    y
    0     a  POINT (0.00000 1.00000)  0.0  1.0
    1     b  POINT (0.00000 2.00000)  0.0  2.0
    2     c  POINT (0.00000 3.00000)  0.0  3.0

    Get the x and y coordinates of each point as a tuple.

    >>> df.xy(frame=False, name="coord")
      label                 geometry       coord
    0     a  POINT (0.00000 1.00000)  (0.0, 1.0)
    1     b  POINT (0.00000 2.00000)  (0.0, 2.0)
    2     c  POINT (0.00000 3.00000)  (0.0, 3.0)

    Set ``reverse=True`` to return (y, x).

    >>> df.xy(reverse=True, frame=False, name="coord")
      label                 geometry       coord
    0     a  POINT (0.00000 1.00000)  (1.0, 0.0)
    1     b  POINT (0.00000 2.00000)  (2.0, 0.0)
    2     c  POINT (0.00000 3.00000)  (3.0, 0.0)
    """

    return pd.concat(
        (
            df,
            s_xy(df.geometry, reverse=reverse, frame=frame, name=name),
        ),
        axis=1,
    )
