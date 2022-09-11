from __future__ import annotations

from typing import get_args
from typing import Literal

import geopandas as gpd
import numpy as np
import pandas as pd
from geopandas.base import GeometryArray
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.register import register_geoseries_method


CHINA_CRS = Literal["wgs84", "gcj02", "bd09"]


@register_geoseries_method
@doc(klass="GeoSeries")
def cncrs_offset(
    s: gpd.GeoSeries,
    /,
    from_crs: CHINA_CRS,
    to_crs: CHINA_CRS,
    a: float = 6378245,
    ee: float = 0.00669342162296594323,
) -> gpd.GeoSeries:
    r"""
    Fix the offset of the coordinates in China.

    Details see: `Restrictions on geographic data in China`__.

    __ https://en.wikipedia.org/wiki/Restrictions_on_geographic_data_in_China

    The following CRS could be transformed:

    - ``WGS-84`` to ``GCJ-02``.
    - ``WGS-84`` to ``BD-09``.
    - ``GCJ-02`` to ``WGS-84``.
    - ``GCJ-02`` to ``BD-09``.
    - ``BD-09`` to ``WGS-84``.
    - ``BD-09`` to ``GCJ-02``.

    Parameters
    ----------
    from_crs, to_crs : {{'wgs84', 'gcj02', 'bd09'}}
        The CRS of the input and output.

    a : float, default 6378245
        Semi major axis of the earth.

    ee : float, default 0.00669342162296594323
        Eccentricity\ :sup:`2`.

    Returns
    -------
    {klass}
        Replaced original geometry.

    Raises
    ------
    ValueError
        If the CRS is not ``ESGP:4326``.

    See Also
    --------
    geopandas.{klass}.to_crs
    dtoolkit.geoaccessor.geoseries.cncrs_offset
    dtoolkit.geoaccessor.geodataframe.cncrs_offset

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd
    >>> df = pd.DataFrame(
    ...     {{
    ...         "x": [114.21892734521, 128.543, 1],
    ...         "y": [29.575429778924, 37.065, 1],
    ...     }},
    ... ).from_xy("x", "y", crs=4326)
    >>> df
                x         y                    geometry
    0  114.218927  29.57543  POINT (114.21893 29.57543)
    1  128.543000  37.06500  POINT (128.54300 37.06500)
    2    1.000000   1.00000     POINT (1.00000 1.00000)
    >>> df.cncrs_offset(from_crs="bd09", to_crs="gcj02")
                x         y                    geometry
    0  114.218927  29.57543  POINT (114.21243 29.56938)
    1  128.543000  37.06500  POINT (128.53659 37.05875)
    2    1.000000   1.00000     POINT (1.00000 1.00000)
    """
    if s.crs != 4326:
        raise ValueError(f"Only support 'EPSG:4326' CRS, but got {s.crs!r}.")
    if from_crs == to_crs:
        raise ValueError("'from_crs' and 'to_crs' must be different.")
    elif from_crs not in get_args(CHINA_CRS):
        raise ValueError(
            f"Unknown 'from_crs': {from_crs!r}, must be in {get_args(CHINA_CRS)!r}.",
        )
    elif to_crs not in get_args(CHINA_CRS):
        raise ValueError(
            f"Unknown 'to_crs': {to_crs!r}, must be in {get_args(CHINA_CRS)!r}.",
        )

    s = s.copy()
    mask = (s.geom_type == "Point") & (is_in_china(s))
    if from_crs == "wgs84" and to_crs == "gcj02":
        s[mask] = wgs84_to_gcj02(s[mask], a=a, ee=ee)
    elif from_crs == "wgs84" and to_crs == "bd09":
        s[mask] = wgs84_to_bd09(s[mask], a=a, ee=ee)
    elif from_crs == "gcj02" and to_crs == "wgs84":
        s[mask] = gcj02_to_wgs84(s[mask], a=a, ee=ee)
    elif from_crs == "gcj02" and to_crs == "bd09":
        s[mask] = gcj02_to_bd09(s[mask])
    elif from_crs == "bd09" and to_crs == "wgs84":
        s[mask] = bd09_to_wgs84(s[mask], a=a, ee=ee)
    elif from_crs == "bd09" and to_crs == "gcj02":
        s[mask] = bd09_to_gcj02(s[mask])

    return s


def is_in_china(s: gpd.GeoSeries, /) -> pd.Series:
    """
    Based on China boundary to judge whether a point is in China.

    Parameters
    ----------
    GeoSeries
        The ESGP:4326 coordinates of the point.

    Returns
    -------
    Series of bool
    """
    from shapely.geometry import box

    return s.covered_by(box(73.66, 3.86, 135.05, 53.55))


# based on https://github.com/wandergis/coordTransform_py
def wgs84_to_gcj02(
    s: gpd.GeoSeries | GeometryArray,
    /,
    a: float,
    ee: float,
) -> GeometryArray:
    rad_y = s.y / 180 * np.pi
    magic = np.sqrt(1 - ee * np.sin(rad_y) ** 2)

    dx = transform_x(s) * 180 / (a / magic * np.cos(rad_y) * np.pi)
    dy = transform_y(s) * 180 / (a * (1 - ee) / magic**3 * np.pi)
    return gpd.points_from_xy(
        x=s.x + dx,
        y=s.y + dy,
    )


def wgs84_to_bd09(
    s: gpd.GeoSeries | GeometryArray,
    /,
    a: float,
    ee: float,
) -> GeometryArray:
    return gcj02_to_bd09(wgs84_to_gcj02(s, a=a, ee=ee))


# based on https://github.com/wandergis/coordTransform_py
def gcj02_to_wgs84(
    s: gpd.GeoSeries | GeometryArray,
    /,
    a: float,
    ee: float,
) -> GeometryArray:
    rad_y = s.y / 180 * np.pi
    magic = np.sqrt(1 - ee * np.sin(rad_y) ** 2)

    dx = transform_x(s) * 180 / (a / magic * np.cos(rad_y) * np.pi)
    dy = transform_y(s) * 180 / ((a * (1 - ee)) / magic**3 * np.pi)
    return gpd.points_from_xy(
        x=s.x - dx,
        y=s.y - dy,
    )


# based on https://github.com/wandergis/coordTransform_py
def transform_x(s: gpd.GeoSeries | GeometryArray, /) -> pd.Series:
    x, y = s.x - 105, s.y - 35
    x_dot_pi = x * np.pi

    return (
        300
        + x
        + 2 * y
        + 0.1 * x**2
        + 0.1 * x * y
        + 0.1 * np.sqrt(np.fabs(x))
        + (20 * np.sin(x_dot_pi * 6) + 20 * np.sin(x_dot_pi * 2)) * 2 / 3
        + (20 * np.sin(x_dot_pi) + 40 * np.sin(x_dot_pi / 3)) * 2 / 3
        + (150 * np.sin(x_dot_pi / 12) + 300 * np.sin(x_dot_pi / 30)) * 2 / 3
    )


# based on https://github.com/wandergis/coordTransform_py
def transform_y(s: gpd.GeoSeries | GeometryArray, /) -> pd.Series:
    x, y = s.x - 105, s.y - 35
    x_dot_pi, y_dot_pi = x * np.pi, y * np.pi

    return (
        -100
        + 2 * x
        + 3 * y
        + 0.2 * y**2
        + 0.1 * x * y
        + 0.2 * np.sqrt(np.fabs(x))
        + (20 * np.sin(x_dot_pi * 6) + 20 * np.sin(x_dot_pi * 2)) * 2 / 3
        + (20 * np.sin(y_dot_pi) + 40 * np.sin(y_dot_pi / 3)) * 2 / 3
        + (160 * np.sin(y_dot_pi / 12) + 320 * np.sin(y_dot_pi / 30)) * 2 / 3
    )


# based on https://github.com/wandergis/coordTransform_py
def gcj02_to_bd09(s: gpd.GeoSeries | GeometryArray, /) -> GeometryArray:
    PI = np.pi * 3000 / 180
    z = np.sqrt(s.x**2 + s.y**2) + 2e-5 * np.sin(s.y * PI)

    theta = np.arctan2(s.y, s.x) + 3e-6 * np.cos(s.x * PI)
    return gpd.points_from_xy(
        x=z * np.cos(theta) + 0.0065,
        y=z * np.sin(theta) + 0.006,
    )


def bd09_to_wgs84(
    s: gpd.GeoSeries | GeometryArray,
    /,
    a: float,
    ee: float,
) -> GeometryArray:
    return gcj02_to_wgs84(bd09_to_gcj02(s), a=a, ee=ee)


# based on https://github.com/wandergis/coordTransform_py
def bd09_to_gcj02(s: gpd.GeoSeries, /) -> GeometryArray:
    PI = np.pi * 3000 / 180
    x, y = s.x - 0.0065, s.y - 0.006
    z = np.sqrt(x**2 + y**2) - 2e-5 * np.sin(y * PI)

    theta = np.arctan2(y, x) - 3e-6 * np.cos(x * PI)
    return gpd.points_from_xy(
        x=z * np.cos(theta),
        y=z * np.sin(theta),
    )
