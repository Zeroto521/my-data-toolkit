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
    Returns a ``Series`` containing the `great-circle`__ distance to aligned other
    via haversine formula.

    __ https://en.wikipedia.org/wiki/Great-circle_distance

    .. math::

        D(x, y) = 2 \\arcsin [
            \\sqrt{
                \\sin^2 ((x_1 - y_1) / 2)
                + \\cos(x_1) \\cos(y_1) \\sin^2 ((x_2 - y_2) / 2)
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
    - The great-circle distance is the angular distance between two points on the
      surface of a sphere. As the Earth is nearly spherical, the haversine formula
      provides a good approximation of the distance between two points of the Earth
      surface, with a less than 1% error on average.

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

        if align and not s.index.equals(other.index):
            warn("The indices are different.", stacklevel=find_stack_level())
            s, other = s.align(other)

        # Force convert to GeoSeries
        other = other.geometry

    return pd.Series(
        radius
        * distance(
            s.geometry.x.to_numpy(),
            s.geometry.y.to_numpy(),
            other.x if isinstance(other, BaseGeometry) else other.x.to_numpy(),
            other.y if isinstance(other, BaseGeometry) else other.y.to_numpy(),
        ),
        index=s.index,
    )


# based on https://github.com/geopy/geopy geopy/distance.py::great_circle.measure
def distance(X, Y):
    """
    Compute the paired the great-circle distance between two points on the earth via
    haversine formula.

    .. math::

        D(x, y) = 2 \\arcsin [
            \\sqrt{
                \\sin^2 ((x_1 - y_1) / 2)
                + \\cos(x_1) \\cos(y_1) \\sin^2 ((x_2 - y_2) / 2)
            }
        ]

    Parameters
    ----------
    X : array-like of shape (n_samples_X, 2)
        A feature array.

    Y : array-like of shape (n_samples_Y, 2)
        An optional second feature array. If None, uses ``Y=X``.

    Returns
    -------
    ndarray

    Raises
    ------
    ValueError
        The dimension of 'X' or 'Y' is not 2.

    Notes
    -----
    - The first coordinate of each point is assumed to be the longitude, the second is
      the latitude, given in radians.
    - The dimension of the data must be 2.

    Examples
    --------
    >>> import numpy as np
    >>> bsas = np.radians([-34.83333, -58.5166646])
    >>> paris = np.radians([49.0083899664, 2.53844117956])
    >>> distance(bsas, paris) * 6371  # multiply by Earth radius to get kilometers
    array([11099.54035582])
    """

    X, Y = np.atleast_2d(X), np.atleast_2d(Y)
    if X.ndim != 2 or Y.ndim != 2:
        raise ValueError("The dimension of the data is not 2.")
    elif X.shape[1] != 2 or Y.shape[1] != 2:
        raise ValueError("The shape of the data must be like (n, 2).")

    lng1, lat1, lng2, lat2 = X[:, 0], X[:, 1], Y[:, 0], Y[:, 1]
    sin_lat1, cos_lat1 = np.sin(lat1), np.cos(lat1)
    sin_lat2, cos_lat2 = np.sin(lat2), np.cos(lat2)

    delta_lng = lng2 - lng1
    cos_delta_lng, sin_delta_lng = np.cos(delta_lng), np.sin(delta_lng)

    return np.arctan2(
        np.sqrt(
            (cos_lat1 * sin_lat2 - sin_lat1 * cos_lat2 * cos_delta_lng) ** 2
            + (cos_lat2 * sin_delta_lng) ** 2,
        ),
        sin_lat1 * sin_lat2 + cos_lat1 * cos_lat2 * cos_delta_lng,
    )
