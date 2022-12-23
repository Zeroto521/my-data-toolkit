from __future__ import annotations

from typing import Hashable

import geopandas as gpd
import pandas as pd

from dtoolkit.geoaccessor.register import register_geoseries_method
from dtoolkit.util._decorator import warning


@register_geoseries_method
@warning(
    "The keyword argument 'x' and 'y' is deprecated, "
    "please use 'names' instead. (Warning added DToolKit 0.0.20)",
    category=DeprecationWarning,
    stacklevel=3,
)
@warning(
    "The keyword argument 'frame' is set to True by default. "
    "(Warning added DToolKit 0.0.20)",
    stacklevel=3,
)
@warning(
    "The keyword argument 'drop' is deprecated, please use "
    "'.drop_geometry' method instead. (Warning added DToolKit 0.0.20)",
    category=DeprecationWarning,
    stacklevel=3,
)
def xy(
    s: gpd.GeoSeries,
    /,
    reverse: bool = False,
    frame: bool = True,
    name: Hashable | tuple[Hashable, Hashable] = ("x", "y"),
) -> gpd.GeoDataFrame:
    """
    Return the x and y location of Point geometries in a GeoSeries.

    Parameters
    ----------
    reverse : bool, default False
        If True, return (y, x) instead.

    frame : bool, default True
        If True, return a DataFrame.

        .. versionchanged:: 0.0.20
            The default value of ``frame`` is set to True.

    drop : bool, default True
        If True, drop the original geometry column.

        .. deprecated:: 0.0.20
            If you want to drop geometry column, please use
            :meth:`~dtoolkit.geoaccessor.geodataframe.drop_geometry` method instead.

    name : Hashable or a tuple of Hashable, default ('x', 'y')
        If ``frame=True``, the column names of the returned DataFrame,
        else the name of the returned Series.

    x : str, default 'x'
        Name of the x column if frame=True.

        .. deprecated:: 0.0.20
            Please use 'name' instead.

    y : str, default 'y'
        Name of the y column if frame=True.

        .. deprecated:: 0.0.20
            Please use 'name' instead.

    Returns
    -------
    GeoDataFrame

    See Also
    --------
    geopandas.GeoSeries.x
    geopandas.GeoSeries.y
    dtoolkit.geoaccessor.geodataframe.xy

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

    Set ``frame=True`` to return a GeoDataFrame with x and y columns.

    >>> s.xy()
         x    y                 geometry
    0  0.0  1.0  POINT (0.00000 1.00000)
    1  0.0  2.0  POINT (0.00000 2.00000)
    2  0.0  3.0  POINT (0.00000 3.00000)

    Get the x and y coordinates of each point as a tuple.

    >>> s.xy(frame=False, name="coord")
            coord                 geometry
    0  (0.0, 1.0)  POINT (0.00000 1.00000)
    1  (0.0, 2.0)  POINT (0.00000 2.00000)
    2  (0.0, 3.0)  POINT (0.00000 3.00000)

    Set ``reverse=True`` to return (y, x).

    >>> s.xy(reverse=True, frame=False, name="coord")
            coord                 geometry
    0  (1.0, 0.0)  POINT (0.00000 1.00000)
    1  (2.0, 0.0)  POINT (0.00000 2.00000)
    2  (3.0, 0.0)  POINT (0.00000 3.00000)
    """

    coords = pd.concat((s.x, s.y), axis=1)
    if frame:
        coords = coords.set_axis(name, axis=1)
    if reverse:
        coords = coords.iloc[:, ::-1]
    if not frame:
        coords = coords.apply(tuple, axis=1).rename(name)

    return coords.to_geoframe(s)
