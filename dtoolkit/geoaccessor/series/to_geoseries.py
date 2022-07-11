from __future__ import annotations

from typing import TYPE_CHECKING

import geopandas as gpd
import pandas as pd
from geopandas.base import is_geometry_type

from dtoolkit.accessor.register import register_series_method

if TYPE_CHECKING:
    from pyproj import CRS


@register_series_method
def to_geoseries(
    s: pd.Series,
    crs: CRS | str | int = None,
    **kwargs,
) -> gpd.GeoSeries | pd.Series:
    """
    Transform an array of shapely scalars :class:`~pandas.Series` to
    a :class:`~geopandas.GeoSeries`.

    Parameters
    ----------
    crs : CRS, str, int, optional
        Coordinate Reference System of the geometry objects. Can be anything
        accepted by :meth:`~pyproj.crs.CRS.from_user_input`, such as an authority
        string (eg "EPSG:4326" / 4326) or a WKT string.

    **kwargs
        See the documentation for :class:`~geopandas.GeoSeries` and  for complete
        details on the keyword arguments.

    Returns
    -------
    GeoSeries or Series
        GeoSeries if the data is an array of shapely scalars.

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd
    >>> s = (
    ...     pd.Series(
    ...         [
    ...             "POINT (1 1)",
    ...             "POINT (2 2)",
    ...             "POINT (3 3)",
    ...         ],
    ...     )
    ...     .from_wkt(drop=True, crs=4326)
    ... )
    >>> s = pd.Series(s)
    >>> s
    0    POINT (1.00000 1.00000)
    1    POINT (2.00000 2.00000)
    2    POINT (3.00000 3.00000)
    dtype: geometry
    >>> type(s)
    <class 'pandas.core.series.Series'>
    >>> gs = s.to_geoseries()
    >>> gs
    0    POINT (1.00000 1.00000)
    1    POINT (2.00000 2.00000)
    2    POINT (3.00000 3.00000)
    dtype: geometry
    >>> type(gs)
    <class 'geopandas.geoseries.GeoSeries'>
    """

    if is_geometry_type(s):
        # Use `.copy` to avoid mutating the original Series.
        s = gpd.GeoSeries(s.copy(), crs=crs, **kwargs)

        # If `s` already has CRS, and it's not the same as `crs`.
        # Then we need to transform it to the CRS the user set.
        if crs is not None and s.crs != crs:
            s = s.to_crs(crs)

    return s
