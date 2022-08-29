from __future__ import annotations

from typing import Hashable
from typing import TYPE_CHECKING

import geopandas as gpd
import pandas as pd

from dtoolkit.accessor.dataframe import drop_or_not  # noqa: F401
from dtoolkit.accessor.register import register_dataframe_method

if TYPE_CHECKING:
    from pyproj import CRS


@register_dataframe_method
def from_wkb(
    df: pd.DataFrame,
    /,
    geometry: Hashable,
    crs: CRS | str | int = None,
    drop: bool = False,
) -> gpd.GeoDataFrame:
    """
    Generate :obj:`~geopandas.GeoDataFrame` of geometries from 'WKB' column of
    :obj:`~pandas.DataFrame`.

    A sugary syntax wraps :meth:`geopandas.GeoSeries.from_wkb`.

    Parameters
    ----------
    geometry : Hashable
        The name of WKB column.

    crs : CRS, str, int, optional
        Coordinate Reference System of the geometry objects. Can be anything
        accepted by :meth:`~pyproj.crs.CRS.from_user_input`, such as an authority
        string (eg "EPSG:4326" / 4326) or a WKT string.

    drop : bool, default False
        Don't contain ``x``, ``y`` and ``z`` anymore.

    Returns
    -------
    GeoDataFrame

    See Also
    --------
    geopandas.GeoSeries.from_wkb
    dtoolkit.geoaccessor.series.from_wkb
    dtoolkit.geoaccessor.dataframe.from_wkt

    Notes
    -----
    - This method is the accessor of DataFrame, not GeoDataFrame.
    - Read from file (such as "CSV" or "EXCEL"), requreis converting "WKB" columns
      type from ``str`` to ``bytes`` via ``eval``.

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd
    >>> s = pd.Series(
    ...      [
    ...          "POINT (1 1)",
    ...          "POINT (2 2)",
    ...          "POINT (3 3)",
    ...      ],
    ...      name="wkt",
    ... )
    >>> s
    0    POINT (1 1)
    1    POINT (2 2)
    2    POINT (3 3)
    Name: wkt, dtype: object
    >>> s_wkb = s.from_wkt(crs=4326, drop=True).to_wkb().rename('wkb')
    >>> s_wkb  # doctest: +SKIP
    0    b'\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00...'
    1    b'\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00...'
    2    b'\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00...'
    Name: wkb, dtype: object
    >>> type(s_wkb)
    <class 'pandas.core.series.Series'>
    >>> gdf = s_wkb.to_frame().from_wkb("wkb", crs=4326)
    >>> gdf  # doctest: +SKIP
                                                      wkb                 geometry
    0  b'\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00...'  POINT (1.00000 1.00000)
    1  b'\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00...'  POINT (2.00000 2.00000)
    2  b'\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00...'  POINT (3.00000 3.00000)
    >>> type(gdf)
    <class 'geopandas.geodataframe.GeoDataFrame'>

    Drop original 'wkb' column.

    >>> gdf = s_wkb.to_frame("wkb").from_wkb("wkb", crs=4326, drop=True)
    >>> gdf
                      geometry
    0  POINT (1.00000 1.00000)
    1  POINT (2.00000 2.00000)
    2  POINT (3.00000 3.00000)
    >>> type(gdf)
    <class 'geopandas.geodataframe.GeoDataFrame'>
    """

    # Avoid mutating the original DataFrame.
    # https://github.com/geopandas/geopandas/issues/1179
    return gpd.GeoDataFrame(
        df.copy().drop_or_not(drop=drop, columns=geometry),
        geometry=gpd.GeoSeries.from_wkb(df[geometry]),
        crs=crs,
    )
