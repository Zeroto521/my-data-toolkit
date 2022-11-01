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
                \\sin^2 ((y_2 - y_1) / 2)
                + \\cos(y_1) \\cos(y_1) \\sin^2 ((x_2 - y_1) / 2)
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

    Calculate the great-circle distance of paired points.

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

    if isinstance(other, BaseGeometry):
        x2, y2 = other.x, other.y
    elif isinstance(other, gpd.base.GeoPandasBase):
        if other.crs != 4326:
            raise ValueError(f"Only support 'EPSG:4326' CRS, but got {other.crs!r}.")
        if align and not s.index.equals(other.index):
            warn("The indices are different.", stacklevel=find_stack_level())
            s, other = s.align(other)

        x2, y2 = other.geometry.x.to_numpy(), other.geometry.y.to_numpy()
    else:
        raise TypeError(f"Unknown type: {type(other).__name__!r}.")

    x1, y1 = s.x.to_numpy(), s.y.to_numpy()
    return pd.Series(
        radius * haversine(x1, y1, x2, y2),
        index=s.index,
    )


def haversine(x1, y1, x2, y2) -> np.ndarray | float:
    """
    Compute the paired the great-circle distance between two points on the earth via
    haversine formula.

    .. math::

        D(x, y) = 2 \\arcsin [
            \\sqrt{
                \\sin^2 ((y_2 - y_1) / 2)
                + \\cos(y_1) \\cos(y_1) \\sin^2 ((x_2 - y_1) / 2)
            }
        ]

    Parameters
    ----------
    x1, y1 : array-like or float
        A feature array. The shape of data should be equal.

    x2, y2 : array-like or float
        A second feature array. The shape of data should be equal.

    Returns
    -------
    ndarray or float

    Notes
    -----
    The first coordinate of each point is assumed to be the longitude, the second is
    the latitude.

    Examples
    --------
    >>> bsas = [-58.5166646, -34.83333]
    >>> paris = [2.53844117956, 49.0083899664]

    Multiply by Earth radius to get kilometers

    >>> int(haversine(*bsas, *paris) * 63711)
    110997
    """

    x1, y1, x2, y2 = map(np.radians, (x1, y1, x2, y2))
    return 2 * np.arcsin(
        np.sqrt(
            np.sin((y2 - y1) / 2) ** 2
            + np.cos(y1) * np.cos(y2) * np.sin((x2 - x1) / 2) ** 2,
        ),
    )
