from warnings import warn

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry.base import BaseGeometry

from dtoolkit.geoaccessor.register import register_geoseries_method
from dtoolkit.util._exception import find_stack_level


def _azimuth(
    x1: np.ndarray | float,
    y1: np.ndarray | float,
    x2: np.ndarray | float,
    y2: np.ndarray | float,
) -> np.ndarray | float:
    """
    Compute the paired great-circle azimuth (initial bearing) between two points
    on the earth.

    The first coordinate of each point is assumed to be the longitude, the second
    is the latitude.

    .. math::

        \\theta = \\texttt{atan2}(
            \\sin(\\Delta\\lambda) \\cdot \\cos(\\varphi_2), \\\\
            \\cos(\\varphi_1) \\cdot \\sin(\\varphi_2)
            - \\sin(\\varphi_1) \\cdot \\cos(\\varphi_2) \\cdot \\cos(\\Delta\\lambda)
        )

    Parameters
    ----------
    x1, y1 : array-like or float
        A feature array. The shape of data should be equal.

    x2, y2 : array-like or float
        A second feature array. The shape of data should be equal.

    Returns
    -------
    ndarray or float
        Azimuth (degrees) in range ``[0, 360)``.

    Examples
    --------
    >>> round(float(_azimuth(116.4, 39.9, 120, 30)), 6)
    162.343098
    """
    x1, y1, x2, y2 = map(np.radians, (x1, y1, x2, y2))
    dlon = x2 - x1
    x = np.sin(dlon) * np.cos(y2)
    y = np.cos(y1) * np.sin(y2) - np.sin(y1) * np.cos(y2) * np.cos(dlon)
    return np.degrees(np.arctan2(x, y)) % 360


@register_geoseries_method
def geoazimuth(
    s: gpd.GeoSeries,
    /,
    other: BaseGeometry | gpd.GeoSeries | gpd.GeoDataFrame,
    align: bool = True,
) -> pd.Series:
    """
    Returns a ``Series`` containing the great-circle azimuth (initial bearing) to
    aligned ``other``.

    Azimuth is measured clockwise from north, in the range ``[0, 360)``.

    .. math::

        \\theta = \\texttt{atan2}(
            \\sin(\\Delta\\lambda) \\cdot \\cos(\\varphi_2), \\\\
            \\cos(\\varphi_1) \\cdot \\sin(\\varphi_2)
            - \\sin(\\varphi_1) \\cdot \\cos(\\varphi_2) \\cdot \\cos(\\Delta\\lambda)
        )

    Parameters
    ----------
    other : BaseGeometry, GeoSeries, or GeoDataFrame

    align : bool, default True
        If True, automatically aligns GeoSeries based on their indices. If False,
        the order of elements is preserved.

    Returns
    -------
    Series(float64)
        Azimuth (degrees) between each pair of points, in range ``[0, 360)``.

    Raises
    ------
    ValueError
        If the CRS is not ``EPSG:4326``.

    TypeError
        If the other is not a ``BaseGeometry``, ``GeoSeries``, or ``GeoDataFrame``.

    See Also
    --------
    dtoolkit.geoaccessor.geoseries.geoazimuth
    dtoolkit.geoaccessor.geoseries.geoazimuth_matrix
    dtoolkit.geoaccessor.geodataframe.geoazimuth
    dtoolkit.geoaccessor.geodataframe.geoazimuth_matrix
    dtoolkit.geoaccessor.geoseries.geodistance

    Notes
    -----
    - Currently, only supports Point geometry.
    - ``0°`` indicates due north, ``90°`` due east, ``180°`` due south,
      ``270°`` due west.

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd
    >>> import geopandas as gpd
    >>> from shapely import Point
    >>> df = (
    ...     pd.DataFrame({"x": [116.4, 121.5], "y": [39.9, 31.2]})
    ...     .from_xy("x", "y", crs=4326)
    ... )
    >>> df
         x    y             geometry
    0  116.4  39.9  POINT (116.4 39.9)
    1  121.5  31.2  POINT (121.5 31.2)
    >>> df.geoazimuth(Point(120, 30))
    0    162.343098
    1    227.478645
    dtype: float64

    Calculate the great-circle azimuth of paired points.

    >>> s = gpd.GeoSeries([Point(120, 30), Point(110, 40)], index=[0, 1], crs=4326)
    >>> s
    0    POINT (120 30)
    1    POINT (110 40)
    dtype: geometry
    >>> df.geoazimuth(s)
    0    162.343098
    1    316.502506
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

    return pd.Series(
        _azimuth(s.x.to_numpy(), s.y.to_numpy(), x2, y2),
        index=s.index,
    )
