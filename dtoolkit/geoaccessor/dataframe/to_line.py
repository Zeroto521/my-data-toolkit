from __future__ import annotations

from collections.abc import Hashable
from typing import TYPE_CHECKING

import geopandas as gpd
import pandas as pd
from shapely import LineString

if TYPE_CHECKING:
    from pyproj import CRS


def to_line(
    df: pd.DataFrame,
    /,
    x1: Hashable,
    y1: Hashable,
    x2: Hashable,
    y2: Hashable,
    crs: CRS | str | int = 4326,
) -> gpd.GeoDataFrame:
    """
    Create a GeoDataFrame with LineString geometries from coordinate columns.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing coordinate columns.

    x1, y1 : Hashable
        Column names for the start (x1, y1) coordinates.

    x2, y2 : Hashable
        Column names for the end (x2, y2) coordinates.

    crs : CRS, str, int, default 4326
        Coordinate reference system for the GeoDataFrame.

    Returns
    -------
    gpd.GeoDataFrame
        GeoDataFrame with LineString geometries.

    See Also
    --------
    shapely.LineString

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd
    >>> df = pd.DataFrame(
    ... {
    ...     "x1": [113.030592, 117.060651],
    ...     "y1": [23.108612, 39.139387],
    ...     "x2": [113.10078400, 23.04620000],
    ...     "y2": [117.23425, 39.378297]
    ... })
    >>> df
               x1         y1          x2          y2
    0  113.030592  23.108612  113.100784  117.234250
    1  117.060651  39.139387   23.046200   39.378297
    >>> df.to_line("x1", "y1", "x2", "y2")
               x1  ...                                           geometry
    0  113.030592  ...  LINESTRING (113.03059 23.10861, 113.10078 117....
    1  117.060651  ...   LINESTRING (117.06065 39.13939, 23.0462 39.3783)

    [2 rows x 5 columns]
    """

    return pd.concat(
        (
            df,
            df.apply(
                lambda s: LineString([s[[x1, y1]], s[[x2, y2]]]),
                axis=1,
            ).rename("geometry"),
        ),
        axis=1,
    ).to_geoframe(crs=crs)
