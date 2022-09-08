from __future__ import annotations

from warnings import warn

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry.base import BaseGeometry

from dtoolkit.geoaccessor.register import register_geoseries_method
from dtoolkit.util._exception import find_stack_level


@register_geoseries_method
def geodistance(
    s: gpd.GeoSeries,
    /,
    other: BaseGeometry | gpd.GeoSeries | gpd.GeoDataFrame,
    align: bool = True,
    radius: float = 6371008.7714150598,
) -> pd.Series:
    """
    Returns a ``Series`` containing the `great-circle`__ distance to aligned other.

    __ https://en.wikipedia.org/wiki/Great-circle_distance

    The algorithm uses the Vincenty formula which is more accurate than the Haversine
    formula.

    .. math::

        D(x, y) = \\arctan[
            \\frac{
                \\sqrt{
                    (
                        \\cos(y_1) \\sin(y_2)
                        - \\sin(y_1) \\cos(y_2) \\cos(x_2 - x_1)
                    )^2
                    + (\\cos(y_2) \\sin(x_2 - x_1))^2
                }
            }{
                \\sin(y_1) \\sin(y_2)
                + \\cos(y_1) \\cos(y_2) \\cos(x_2 - x_1)
            }
        ]

    Parameters
    ----------
    other : BaseGeometry, GeoSeries, or GeoDataFrame

    align : bool, default True
        If True, automatically aligns GeoSeries based on their indices. If False,
        the order of elements is preserved.

    radius : float, default 6371008.7714150598
        Great-circle distance uses a spherical model of the earth, using the mean earth
        radius as defined by the International Union of Geodesy and Geophysics,
        (2\\ *a* + *b*)/3 = 6371008.7714150598 meters for WGS-84.

    Returns
    -------
    Series
        The values are the great-circle distances and its unit is meters.

    Raises
    ------
    ValueError
        If the CRS is not ``ESGP:4326``.

    TypeError
        If the other is not a ``BaseGeometry``, ``GeoSeries``, or ``GeoDataFrame``.

    See Also
    --------
    geopandas.GeoSeries.distance
    dtoolkit.geoaccessor.geoseries.geodistance
    dtoolkit.geoaccessor.geoseries.geodistance_matrix
    dtoolkit.geoaccessor.geodataframe.geodistance
    dtoolkit.geoaccessor.geodataframe.geodistance_matrix

    Notes
    -----
    - Currently, only supports Point geometry.
    - The geodesic distance is the shortest distance on the surface of an ellipsoidal
      model of the earth. Resulting in an error of up to about 0.5%.

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd
    >>> import geopandas as gpd
    >>> from shapely.geometry import Point
    >>> df = (
    ...     pd.DataFrame({"x": [122, 100], "y":[55, 1]})
    ...     .from_xy("x", "y", crs=4326)
    ... )
    >>> df
         x   y                    geometry
    0  122  55  POINT (122.00000 55.00000)
    1  100   1   POINT (100.00000 1.00000)
    >>> df.geodistance(Point(120, 30)) / 1e6
    0    2.784435
    1    3.855604
    dtype: float64

    Calculate the great-circle distance of corresponding points.

    >>> s = gpd.GeoSeries([Point(120, 30), Point(120, 50)], index=[1, 2], crs=4326)
    >>> s
    1    POINT (120.00000 30.00000)
    2    POINT (120.00000 50.00000)
    dtype: geometry
    >>> df.geodistance(s) / 1e6
    0         NaN
    1    3.855604
    2         NaN
    dtype: float64
    >>> df.geodistance(s, align=False) / 1e6
    0    2.784435
    1    5.768885
    dtype: float64
    """

    if s.crs != 4326:
        raise ValueError(f"Only support 'EPSG:4326' CRS, but got {s.crs!r}.")
    if not isinstance(other, (BaseGeometry, gpd.base.GeoPandasBase)):
        raise TypeError(f"Unknown type: {type(other).__name__!r}.")

    if isinstance(other, gpd.base.GeoPandasBase):
        if other.crs != 4326:
            raise ValueError(f"Only support 'EPSG:4326' CRS, but got {other.crs!r}.")

        s = s.geometry
        if align and not s.index.equals(other.index):
            warn("The indices are different.", stacklevel=find_stack_level())
            s, other = s.align(other)

        # Force convert to GeoSeries
        other = other.geometry

    return pd.Series(
        distance(
            s.geometry.x.to_numpy(),
            s.geometry.y.to_numpy(),
            other.x if isinstance(other, BaseGeometry) else other.x.to_numpy(),
            other.y if isinstance(other, BaseGeometry) else other.y.to_numpy(),
            radius=radius,
        ),
        index=s.index,
    )


# based on https://github.com/geopy/geopy geopy/distance.py::great_circle.measure
def distance(
    lng1: np.ndarray | float,
    lat1: np.ndarray | float,
    lng2: np.ndarray | float,
    lat2: np.ndarray | float,
    radius: float,
) -> np.ndarray:
    lng1, lat1, lng2, lat2 = map(np.radians, (lng1, lat1, lng2, lat2))
    sin_lat1, cos_lat1 = np.sin(lat1), np.cos(lat1)
    sin_lat2, cos_lat2 = np.sin(lat2), np.cos(lat2)

    delta_lng = lng2 - lng1
    cos_delta_lng, sin_delta_lng = np.cos(delta_lng), np.sin(delta_lng)

    return radius * np.arctan2(
        np.sqrt(
            (cos_lat1 * sin_lat2 - sin_lat1 * cos_lat2 * cos_delta_lng) ** 2
            + (cos_lat2 * sin_delta_lng) ** 2,
        ),
        sin_lat1 * sin_lat2 + cos_lat1 * cos_lat2 * cos_delta_lng,
    )
