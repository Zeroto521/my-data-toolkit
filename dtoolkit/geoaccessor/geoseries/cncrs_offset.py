from typing import get_args
from typing import Literal

import geopandas as gpd
import numpy as np
import shapely
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.register import register_geoseries_method

PI = np.pi * 3000 / 180
CHINA_CRS = Literal["wgs84", "gcj02", "bd09"]
a = 6378245  # Semi major axis of the earth.
ee = 0.00669342162296594323  # Eccentricity\ :sup:`2`.


@register_geoseries_method
@doc(klass="GeoSeries")
def cncrs_offset(
    s: gpd.GeoSeries,
    /,
    from_crs: CHINA_CRS,
    to_crs: CHINA_CRS,
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
    1  128.543000  37.06500      POINT (128.543 37.065)
    2    1.000000   1.00000                 POINT (1 1)
    >>> df.cncrs_offset(from_crs="bd09", to_crs="gcj02")
                x         y                    geometry
    0  114.218927  29.57543  POINT (114.21243 29.56938)
    1  128.543000  37.06500  POINT (128.53659 37.05875)
    2    1.000000   1.00000     POINT (0.99349 0.99399)
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

    if from_crs == "wgs84" and to_crs == "gcj02":
        transformer = wgs84_to_gcj02
    elif from_crs == "wgs84" and to_crs == "bd09":
        transformer = wgs84_to_bd09
    elif from_crs == "gcj02" and to_crs == "wgs84":
        transformer = gcj02_to_wgs84
    elif from_crs == "gcj02" and to_crs == "bd09":
        transformer = gcj02_to_bd09
    elif from_crs == "bd09" and to_crs == "wgs84":
        transformer = bd09_to_wgs84
    elif from_crs == "bd09" and to_crs == "gcj02":
        transformer = bd09_to_gcj02

    s = s.copy()
    return gpd.GeoSeries(
        transform(s, transformer),
        crs=s.crs,
        index=s.index,
        name=s.name,
    )


# based on geopandas.array.transform, fixed for NumPy 2.0 compatibility
def transform(data, func: callable) -> np.ndarray:
    data_copy = np.array(data, copy=True)  # Create a copy to avoid mutation
    res = np.empty_like(data_copy)

    coords = shapely.get_coordinates(data_copy, include_z=True)
    new_x, new_y = func(coords[:, 0], coords[:, 1])

    if coords.shape[1] == 3:  # Has z dimension - preserve it
        new_coords = np.column_stack([new_x, new_y, coords[:, 2]])
    else:  # Only x, y
        new_coords = np.column_stack([new_x, new_y])

    # Ensure array is writable and C-contiguous for NumPy 2.0 compatibility
    new_coords = np.ascontiguousarray(new_coords, dtype=np.float64)
    res[:] = shapely.set_coordinates(data_copy, new_coords)
    return res

# based on https://github.com/wandergis/coordTransform_py
def wgs84_to_gcj02(x: np.array, y: np.array, /, z=None) -> tuple[np.array, np.array]:
    rad_y = y / 180 * np.pi
    magic = np.sqrt(1 - ee * np.sin(rad_y) ** 2)

    dx = transform_x(x, y) * 180 / (a / magic * np.cos(rad_y) * np.pi)
    dy = transform_y(x, y) * 180 / (a * (1 - ee) / magic**3 * np.pi)
    return x + dx, y + dy


def wgs84_to_bd09(x: np.array, y: np.array, /, z=None) -> tuple[np.array, np.array]:
    return gcj02_to_bd09(*wgs84_to_gcj02(x, y, z), z)


# based on https://github.com/wandergis/coordTransform_py
def gcj02_to_wgs84(x: np.array, y: np.array, /, z=None) -> tuple[np.array, np.array]:
    rad_y = y / 180 * np.pi
    magic = np.sqrt(1 - ee * np.sin(rad_y) ** 2)

    dx = transform_x(x, y) * 180 / (a / magic * np.cos(rad_y) * np.pi)
    dy = transform_y(x, y) * 180 / (a * (1 - ee) / magic**3 * np.pi)
    return x - dx, y - dy


# based on https://github.com/wandergis/coordTransform_py
def transform_x(x: np.array, y: np.array, /) -> np.array:
    x_shifted, y_shifted = x - 105, y - 35
    x_dot_pi = x_shifted * np.pi

    return (
        300
        + x_shifted
        + 2 * y_shifted
        + 0.1 * x_shifted**2
        + 0.1 * x_shifted * y_shifted
        + 0.1 * np.sqrt(np.fabs(x_shifted))
        + (20 * np.sin(x_dot_pi * 6) + 20 * np.sin(x_dot_pi * 2)) * 2 / 3
        + (20 * np.sin(x_dot_pi) + 40 * np.sin(x_dot_pi / 3)) * 2 / 3
        + (150 * np.sin(x_dot_pi / 12) + 300 * np.sin(x_dot_pi / 30)) * 2 / 3
    )


# based on https://github.com/wandergis/coordTransform_py
def transform_y(x: np.array, y: np.array, /) -> np.array:
    x_shifted, y_shifted = x - 105, y - 35
    x_dot_pi, y_dot_pi = x_shifted * np.pi, y_shifted * np.pi

    return (
        -100
        + 2 * x_shifted
        + 3 * y_shifted
        + 0.2 * y_shifted**2
        + 0.1 * x_shifted * y_shifted
        + 0.2 * np.sqrt(np.fabs(x_shifted))
        + (20 * np.sin(x_dot_pi * 6) + 20 * np.sin(x_dot_pi * 2)) * 2 / 3
        + (20 * np.sin(y_dot_pi) + 40 * np.sin(y_dot_pi / 3)) * 2 / 3
        + (160 * np.sin(y_dot_pi / 12) + 320 * np.sin(y_dot_pi / 30)) * 2 / 3
    )


# based on https://github.com/wandergis/coordTransform_py
def gcj02_to_bd09(x: np.array, y: np.array, /, z=None) -> tuple[np.array, np.array]:
    d = np.sqrt(x**2 + y**2) + 2e-5 * np.sin(y * PI)
    theta = np.arctan2(y, x) + 3e-6 * np.cos(x * PI)
    return d * np.cos(theta) + 0.0065, d * np.sin(theta) + 0.006


def bd09_to_wgs84(x: np.array, y: np.array, /, z=None) -> tuple[np.array, np.array]:
    return gcj02_to_wgs84(*bd09_to_gcj02(x, y, z), z)


# based on https://github.com/wandergis/coordTransform_py
def bd09_to_gcj02(x: np.array, y: np.array, /, z=None) -> tuple[np.array, np.array]:
    x_shifted = x - 0.0065
    y_shifted = y - 0.006

    d = np.sqrt(x_shifted**2 + y_shifted**2) - 2e-5 * np.sin(y_shifted * PI)
    theta = np.arctan2(y_shifted, x_shifted) - 3e-6 * np.cos(x_shifted * PI)
    return d * np.cos(theta), d * np.sin(theta)
