from __future__ import annotations

from typing import Hashable

import geopandas as gpd
import pandas as pd

from dtoolkit.geoaccessor.geodataframe.drop_geometry import drop_geometry
from dtoolkit.geoaccessor.geoseries import points_to_h3 as s_points_to_h3
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
def points_to_h3(
    df: gpd.GeoDataFrame,
    /,
    resolution: int,
    column: Hashable = "h3",
    drop: bool = True,
) -> pd.DataFrame | gpd.GeoDataFrame:
    """
    Convert Point to containing H3 cell index.

    Parameters
    ----------
    resolution : int
        H3 resolution.

    column : Hashable, default "h3"
        Name of the column to store the H3 cell index.

    drop : bool, default True
        Whether to drop the geometry column.

    Returns
    -------
    DataFrame or GeoDataFrame
        DataFrame if drop is True else GeoDataFrame.

    Raises
    ------
    ModuleNotFoundError
        If don't have module named 'h3'.
    TypeError
        If the geometry is not Point.
    ValueError
        If the CRS is not WGS84 or EPSG:4326.

    See Also
    --------
    h3.latlon_to_h3
    dtoolkit.geoaccessor.geoseries.points_to_h3

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd
    >>> df = pd.DataFrame({"x": [122, 100], "y": [55, 1]}).from_xy('x', 'y', crs=4326)
    >>> df
         x   y                    geometry
    0  122  55  POINT (122.00000 55.00000)
    1  100   1   POINT (100.00000 1.00000)
    >>> df.points_to_h3(8)
         x   y                  h3
    0  122  55  612845052823076863
    1  100   1  614269156845420543
    """

    h3 = s_points_to_h3(df.geometry, resolution, column=column, drop=True)

    if drop:
        df = drop_geometry(df)

    return df.assign(**{column: h3})
