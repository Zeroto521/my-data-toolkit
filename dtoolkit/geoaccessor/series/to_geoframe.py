from __future__ import annotations

from typing import TYPE_CHECKING

import geopandas as gpd
import pandas as pd
from geopandas.base import is_geometry_type

from dtoolkit.accessor.register import register_series_method

if TYPE_CHECKING:
    from pyproj import CRS


@register_series_method
def to_geoframe(
    s: pd.Series,
    /,
    geometry: gpd.GeoSeries = None,
    crs: CRS | str | int = None,
    **kwargs,
) -> gpd.GeoDataFrame | pd.DataFrame:
    """
    Transform an array of shapely scalars :class:`~pandas.Series` to
    a :class:`~geopandas.GeoDataFrame`.

    Parameters
    ----------
    geometry : GeoSeries, optional
        It will be prior set as 'geometry' column on GeoDataFrame.

    crs : CRS, str, int, optional
        Coordinate Reference System of the geometry objects. Can be anything
        accepted by :meth:`~pyproj.crs.CRS.from_user_input`, such as an authority
        string (eg "EPSG:4326" / 4326) or a WKT string.

    **kwargs
        See the documentation for :class:`~geopandas.GeoDataFrame` and  for complete
        details on the keyword arguments.

    Returns
    -------
    DataFrame or GeoDataFrame
        GeoDataFrame if the data is an array of shapely scalars or ``geometry`` is set.

    See Also
    --------
    dtoolkit.geoaccessor.series.to_geoseries
    dtoolkit.geoaccessor.dataframe.to_geoframe

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd
    >>> s = pd.Series(
    ...     pd.Series(
    ...         [
    ...             "POINT (1 1)",
    ...             "POINT (2 2)",
    ...             "POINT (3 3)",
    ...         ],
    ...     )
    ...     .from_wkt(drop=True, crs=4326)
    ... )
    >>> s
    0    POINT (1.00000 1.00000)
    1    POINT (2.00000 2.00000)
    2    POINT (3.00000 3.00000)
    dtype: geometry
    >>> type(s)
    <class 'pandas.core.series.Series'>
    >>> gs = s.to_geoframe()
    >>> gs
                        geometry
    0    POINT (1.00000 1.00000)
    1    POINT (2.00000 2.00000)
    2    POINT (3.00000 3.00000)
    >>> type(gs)
    <class 'geopandas.geodataframe.GeoDataFrame'>
    """

    if geometry is not None:
        return gpd.GeoDataFrame(s, geometry=geometry, crs=crs, **kwargs)
    elif is_geometry_type(s):
        return gpd.GeoDataFrame(geometry=s, crs=crs, **kwargs)
    else:
        return s.to_frame()
