from __future__ import annotations

from typing import Hashable
from typing import TYPE_CHECKING

import geopandas as gpd
import pandas as pd

from dtoolkit.accessor.register import register_dataframe_method

if TYPE_CHECKING:
    from pyproj import CRS


@register_dataframe_method
def to_geoframe(
    df: pd.DataFrame,
    /,
    geometry: Hashable | gpd.GeoSeries = None,
    crs: CRS | str | int = None,
    **kwargs,
) -> gpd.GeoDataFrame:
    """
    Transform a :class:`~pandas.DataFrame` to a :class:`~geopandas.GeoDataFrame`.

    Parameters
    ----------
    geometry : Hashable or GeoSeries, optional
        If str or int, column to use as geometry. If array, will be set as 'geometry'
        column on GeoDataFrame.

    crs : CRS, str, int, optional
        Coordinate Reference System of the geometry objects. Can be anything
        accepted by :meth:`~pyproj.crs.CRS.from_user_input`, such as an authority
        string (eg "EPSG:4326" / 4326) or a WKT string.

    **kwargs
        See the documentation for :class:`~geopandas.GeoDataFrame` and  for complete
        details on the keyword arguments.

    Returns
    -------
    GeoDataFrame

    See Also
    --------
    dtoolkit.geoaccessor.series.to_geoseries
    dtoolkit.geoaccessor.series.to_geoframe

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd
    >>> df_point = (
    ...     pd.DataFrame({"x": [122, 100], "y":[55, 1]})
    ...     .from_xy("x", "y", drop=True, crs=4326)
    ... )
    >>> df_point
                         geometry
    0  POINT (122.00000 55.00000)
    1   POINT (100.00000 1.00000)
    >>> df_data = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    >>> df = pd.concat((df_data, df_point), axis=1)
    >>> df
       a  b                    geometry
    0  1  3  POINT (122.00000 55.00000)
    1  2  4   POINT (100.00000 1.00000)

    ``df`` is DataFrame type not GeoDataFrame type.

    >>> type(df)
    <class 'pandas.core.frame.DataFrame'>

    >>> df = df.to_geoframe()
    >>> df
       a  b                    geometry
    0  1  3  POINT (122.00000 55.00000)
    1  2  4   POINT (100.00000 1.00000)

    ``df`` is GeoDataFrame type at present.

    >>> type(df)
    <class 'geopandas.geodataframe.GeoDataFrame'>

    Use original CRS if its CRS is not specified.

    >>> df.crs == df_point.crs == 4326
    True
    >>> df.crs
    <Geographic 2D CRS: EPSG:4326>
    Name: WGS 84
    Axis Info [ellipsoidal]:
    - Lat[north]: Geodetic latitude (degree)
    - Lon[east]: Geodetic longitude (degree)
    Area of Use:
    - name: World.
    - bounds: (-180.0, -90.0, 180.0, 90.0)
    Datum: World Geodetic System 1984 ensemble
    - Ellipsoid: WGS 84
    - Prime Meridian: Greenwich
    """

    return (
        gpd.GeoDataFrame(
            # Avoid mutating the original DataFrame.
            # https://github.com/geopandas/geopandas/issues/1179
            df.copy(),
            crs=crs,
            geometry=geometry,
            **kwargs,
        )
        if not isinstance(df, gpd.GeoDataFrame)
        else df
    )
