from __future__ import annotations

import geopandas as gpd
import numpy as np
import pandas as pd

from dtoolkit.geoaccessor.geoseries.xy import xy
from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
def geodistance_matrix(
    s: gpd.GeoSeries,
    /,
    other: gpd.GeoSeries | gpd.GeoDataFrame | None = None,
    radius: float = 6371008.7714150598,
) -> pd.DataFrame:
    """
    Returns a ``DataFrame`` containing the `great-circle`__ distances matrix between in
    ``s`` and ``other`` via haversine formula.

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
    other : GeoSeries, or GeoDataFrame, default None
        If None, uses ``other=s``.

    radius : float, default 6371008.7714150598
        Great-circle distance uses a spherical model of the earth, using the mean earth
        radius as defined by the International Union of Geodesy and Geophysics,
        (2\\ *a* + *b*)/3 = 6371008.7714150598 meters for WGS-84.

    Returns
    -------
    DataFrame
        - The index and columns are the same as the index of ``s`` and ``other``.
        - The values are the great-circle distances and its unit is meters.

    Raises
    ------
    ModuleNotFoundError
        If don't have module named 'sklearn'.

    ValueError
        If the CRS is not ``ESGP:4326``.

    TypeError
        If the other is not a GeoSeries, GeoDataFrame, or None type.

    See Also
    --------
    sklearn.metrics.pairwise.haversine_distances
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
    >>> df = pd.DataFrame(
    ...     {
    ...         "x": [120, 122, 100],
    ...         "y":[30, 55, 1],
    ...     },
    ... ).from_xy("x", "y", crs=4326)
    >>> df
         x   y                    geometry
    0  120  30  POINT (120.00000 30.00000)
    1  122  55  POINT (122.00000 55.00000)
    2  100   1   POINT (100.00000 1.00000)
    >>> other = pd.DataFrame(
    ...     {
    ...         "x": [120, 110],
    ...         "y":[30, 40],
    ...     },
    ... ).from_xy("x", "y", crs=4326)
    >>> other
         x   y                    geometry
    0  120  30  POINT (120.00000 30.00000)
    1  110  40  POINT (110.00000 40.00000)
    >>> df.geodistance_matrix(other)
                  0             1
    0  0.000000e+00  1.435335e+06
    1  2.784435e+06  1.889892e+06
    2  3.855604e+06  4.453100e+06
    """
    from sklearn.metrics.pairwise import haversine_distances

    if s.crs != 4326:
        raise ValueError(f"Only support 'EPSG:4326' CRS, but got {s.crs!r}.")

    if other is None:
        Y = None
    elif isinstance(other, gpd.base.GeoPandasBase):
        if other.crs != 4326:
            raise ValueError(f"Only support 'EPSG:4326' CRS, but got {other.crs!r}.")

        Y = np.radians(xy(other.geometry, reverse=True).tolist())
    else:
        raise TypeError(f"Unknown type: {type(other).__name__!r}.")

    X = np.radians(xy(s, reverse=True).tolist())
    return pd.DataFrame(
        radius * haversine_distances(X, Y),
        index=s.index,
        columns=other.index if other is not None else s.index,
    )
