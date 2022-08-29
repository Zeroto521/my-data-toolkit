from __future__ import annotations

from typing import TYPE_CHECKING

import geopandas as gpd
import pandas as pd

from dtoolkit.accessor.register import register_series_method

if TYPE_CHECKING:
    from pyproj import CRS


@register_series_method
def from_wkb(
    s: pd.Series,
    /,
    crs: CRS | str | int = None,
    drop: bool = False,
) -> gpd.GeoSeries | gpd.GeoDataFrame:
    """
    Generate :obj:`~geopandas.GeoDataFrame` of geometries from :obj:`~pandas.Series`.

    A sugary syntax wraps :meth:`geopandas.GeoSeries.from_wkb`.

    Parameters
    ----------
    crs : CRS, str, int, optional
        Coordinate Reference System of the geometry objects. Can be anything
        accepted by :meth:`~pyproj.crs.CRS.from_user_input`, such as an authority
        string (eg "EPSG:4326" / 4326) or a WKT string.

    drop : bool, default False
        Don't contain original WKB anymore.

    Returns
    -------
    GeoSeries or GeoDataFrame
        GeoSeries if `drop` is True else GeoDataFrame.

    Raises
    ------
    ValueError
        If ``drop`` is False and the name of Series is empty.

    See Also
    --------
    geopandas.GeoSeries.from_wkb
    dtoolkit.geoaccessor.series.from_wkt
    dtoolkit.geoaccessor.dataframe.from_wkb

    Notes
    -----
    - This method is the accessor of Series, not GeoSeries.
    - Read from file (such as "CSV" or "EXCEL"), requreis converting "WKB" column
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
    >>> gdf = s_wkb.from_wkb(crs=4326)
    >>> gdf  # doctest: +SKIP
                                                      wkb                 geometry
    0  b'\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00...'  POINT (1.00000 1.00000)
    1  b'\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00...'  POINT (2.00000 2.00000)
    2  b'\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00...'  POINT (3.00000 3.00000)
    >>> type(gdf)
    <class 'geopandas.geodataframe.GeoDataFrame'>

    Drop original 'wkb' column.

    >>> gs = s_wkb.from_wkb(crs=4326, drop=True)
    >>> gs
    0    POINT (1.00000 1.00000)
    1    POINT (2.00000 2.00000)
    2    POINT (3.00000 3.00000)
    dtype: geometry
    >>> type(gs)
    <class 'geopandas.geoseries.GeoSeries'>
    """

    if not drop and s.name is None:
        raise ValueError(
            "to keep the original data requires setting the 'name' of "
            f"{s.__class__.__name__!r}",
        )

    geometry = gpd.GeoSeries.from_wkb(s, crs=crs)
    return geometry if drop else gpd.GeoDataFrame(s, geometry=geometry)
