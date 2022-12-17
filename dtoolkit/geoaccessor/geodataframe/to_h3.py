from __future__ import annotations

from typing import Hashable

import geopandas as gpd
import pandas as pd

from dtoolkit.accessor.dataframe import repeat
from dtoolkit.accessor.series import len as s_len
from dtoolkit.geoaccessor.geodataframe.drop_geometry import drop_geometry
from dtoolkit.geoaccessor.geoseries.to_h3 import points_to_h3
from dtoolkit.geoaccessor.geoseries.to_h3 import polygons_to_h3
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
def to_h3(
    df: gpd.GeoDataFrame,
    /,
    resolution: int,
    drop: bool = True,
    name: Hashable = "h3",
    int_dtype: bool = True,
) -> pd.DataFrame | gpd.GeoDataFrame:
    """
    Convert Point to containing H3 cell index.

    Parameters
    ----------
    resolution : int
        H3 resolution.

    drop : bool, default True
        Whether to drop the geometry column.

    name : Hashable, default "h3"
        Name of the column to store the H3 cell index.

    int_dtype : bool, default True
        If True, use `h3.api.numpy_int` else use `h3.api.basic_str`.

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
    dtoolkit.geoaccessor.geoseries.to_h3

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd

    Points to h3 indexes.

    >>> df = pd.DataFrame({"x": [122, 100], "y": [55, 1]}).from_xy('x', 'y', crs=4326)
    >>> df
         x   y                    geometry
    0  122  55  POINT (122.00000 55.00000)
    1  100   1   POINT (100.00000 1.00000)
    >>> df.to_h3(8)
         x   y                  h3
    0  122  55  612845052823076863
    1  100   1  614269156845420543

    Keep the geometry column.

    >>> df.to_h3(8, drop=False)
         x   y                    geometry                  h3
    0  122  55  POINT (122.00000 55.00000)  612845052823076863
    1  100   1   POINT (100.00000 1.00000)  614269156845420543

    Polygons to h3 indexes.

    >>> df = pd.DataFrame(
    ...     {
    ...         "label": ["a", "b"],
    ...         "wkt": [
    ...             "POLYGON ((1 0, 1 1, 0 1, 0 0, 1 0))",
    ...             "POLYGON ((2 1, 2 2, 1 2, 1 1, 2 1))",
    ...         ],
    ...     },
    ... ).from_wkt("wkt", crs=4326, drop=True)
    >>> df
      label                                           geometry
    0     a  POLYGON ((1.00000 0.00000, 1.00000 1.00000, 0....
    1     b  POLYGON ((2.00000 1.00000, 2.00000 2.00000, 1....
    >>> df.to_h3(4)
      label                  h3
    0     a  596538839648960511
    0     a  596538693620072447
    0     a  596538685030137855
    0     a  596538848238895103
    0     a  596537920525959167
    0     a  596538813879156735
    0     a  596538856828829695
    0     a  596538805289222143
    1     b  596538229763604479
    1     b  596537946295762943
    1     b  596540780974178303
    1     b  596540729434570751
    1     b  596540772384243711
    1     b  596538212583735295
    1     b  596540763794309119
    1     b  596537954885697535
    1     b  596540746614439935
    1     b  596538195403866111
    1     b  596541030082281471
    """

    if df.crs != 4326:
        raise ValueError(f"Only support 'EPSG:4326' CRS, but got {df.crs!r}.")

    if all(df.geom_type == "Point"):
        h3 = points_to_h3(
            df.geometry,
            resolution=resolution,
            int_dtype=int_dtype,
        ).rename(name)
    elif all(df.geom_type == "Polygon"):
        h3_list = polygons_to_h3(
            df.geometry,
            resolution=resolution,
            int_dtype=int_dtype,
        )
        h3 = h3_list.explode().rename(name)
        df = repeat(df, s_len(h3_list))
    else:
        raise TypeError("Only support 'Point' or 'Polygon' geometry type.")

    return pd.concat((drop_geometry(df) if drop else df, h3), axis=1)
