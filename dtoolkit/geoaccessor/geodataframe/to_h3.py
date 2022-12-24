from __future__ import annotations

from typing import Hashable

import geopandas as gpd
import pandas as pd

from dtoolkit.geoaccessor.geoseries import to_h3 as s_to_h3
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
def to_h3(
    df: gpd.GeoDataFrame,
    /,
    resolution: int,
    int_dtype: bool = True,
) -> gpd.GeoDataFrame:
    """
    Convert Point to containing H3 cell index.

    Parameters
    ----------
    resolution : int
        H3 resolution.

    int_dtype : bool, default True
        If True, use ``h3.api.numpy_int`` else use ``h3.api.basic_str``.

    Returns
    -------
    GeoDataFrame
        With H3 cell as the its index.

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
    h3.polygon_to_cells
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
                          x   y                    geometry
    612845052823076863  122  55  POINT (122.00000 55.00000)
    614269156845420543  100   1   POINT (100.00000 1.00000)

    Polygons to h3 indexes.

    >>> df = pd.DataFrame(
    ...     {
    ...         "label": ["a", "b"],
    ...         "wkt": [
    ...             "POLYGON ((1 0, 1 1, 0 1, 0 0, 1 0))",
    ...             "POLYGON ((2 1, 2 2, 1 2, 1 1, 2 1))",
    ...         ],
    ...     },
    ... ).from_wkt("wkt", crs=4326).drop(columns="wkt")
    >>> df
      label                                           geometry
    0     a  POLYGON ((1.00000 0.00000, 1.00000 1.00000, 0....
    1     b  POLYGON ((2.00000 1.00000, 2.00000 2.00000, 1....
    >>> df.to_h3(4)
                        label                                           geometry
    596538839648960511      a  POLYGON ((1.00000 0.00000, 1.00000 1.00000, 0....
    596538693620072447      a  POLYGON ((1.00000 0.00000, 1.00000 1.00000, 0....
    596538685030137855      a  POLYGON ((1.00000 0.00000, 1.00000 1.00000, 0....
    596538848238895103      a  POLYGON ((1.00000 0.00000, 1.00000 1.00000, 0....
    596537920525959167      a  POLYGON ((1.00000 0.00000, 1.00000 1.00000, 0....
    596538813879156735      a  POLYGON ((1.00000 0.00000, 1.00000 1.00000, 0....
    596538856828829695      a  POLYGON ((1.00000 0.00000, 1.00000 1.00000, 0....
    596538805289222143      a  POLYGON ((1.00000 0.00000, 1.00000 1.00000, 0....
    596538229763604479      b  POLYGON ((2.00000 1.00000, 2.00000 2.00000, 1....
    596537946295762943      b  POLYGON ((2.00000 1.00000, 2.00000 2.00000, 1....
    596540780974178303      b  POLYGON ((2.00000 1.00000, 2.00000 2.00000, 1....
    596540729434570751      b  POLYGON ((2.00000 1.00000, 2.00000 2.00000, 1....
    596540772384243711      b  POLYGON ((2.00000 1.00000, 2.00000 2.00000, 1....
    596538212583735295      b  POLYGON ((2.00000 1.00000, 2.00000 2.00000, 1....
    596540763794309119      b  POLYGON ((2.00000 1.00000, 2.00000 2.00000, 1....
    596537954885697535      b  POLYGON ((2.00000 1.00000, 2.00000 2.00000, 1....
    596540746614439935      b  POLYGON ((2.00000 1.00000, 2.00000 2.00000, 1....
    596538195403866111      b  POLYGON ((2.00000 1.00000, 2.00000 2.00000, 1....
    596541030082281471      b  POLYGON ((2.00000 1.00000, 2.00000 2.00000, 1....

    Also support str (hexadecimal) format.

    >>> df = pd.DataFrame({"x": [122, 100], "y": [55, 1]}).from_xy('x', 'y', crs=4326)
    >>> df
         x   y                    geometry
    0  122  55  POINT (122.00000 55.00000)
    1  100   1   POINT (100.00000 1.00000)
    >>> df.to_h3(8, int_dtype=False)
                       x   y                    geometry
    88143541bdfffff  122  55  POINT (122.00000 55.00000)
    886528b2a3fffff  100   1   POINT (100.00000 1.00000)
    """

    return s_to_h3(df, resolution=resolution, int_dtype=int_dtype)
