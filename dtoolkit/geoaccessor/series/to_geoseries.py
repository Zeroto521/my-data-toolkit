from __future__ import annotations

import geopandas as gpd
import pandas as pd
from geopandas.base import is_geometry_type
from pyproj import CRS

from dtoolkit.accessor.register import register_series_method


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
    """

    if is_geometry_type(s):
        crs = CRS.from_user_input(crs)
        # Use `.copy` to avoid mutating the original Series.
        s = gpd.GeoSeries(s.copy(), crs=crs, **kwargs)

        # If `s` already has CRS, and it's not the same as `crs`.
        # Then we need to transform it to the CRS the user set.
        if s.crs != crs:
            s = s.to_crs(crs)

    return s
