from __future__ import annotations

from typing import TYPE_CHECKING
from warnings import catch_warnings
from warnings import filterwarnings
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
    Returns a ``Series`` containing the great-circle distance to aligned other.

    Parameters
    ----------
    other : BaseGeometry, GeoSeries, or GeoDataFrame

    align : bool, default True
        If True, automatically aligns GeoSeries based on their indices. If False,
        the order of elements is preserved.

    radius : float, default 6371008.7714150598
        Great-circle distance uses a spherical model of the earth, using the mean earth
        radius as defined by the International Union of Geodesy and Geophysics,
        (2\\ *a* + *b*)/3 = 6371008.7714150598 meters for WGS-84, resulting in an error
        of up to about 0.5%.

    Returns
    -------
    Series

    Raises
    ------
    ValueError
        If the CRS is not ``ESGP:4326``.

    See Also
    --------
    geopandas.GeoSeries.distance
    sklearn.metrics.pairwise.haversine_distances

    Notes
    -----
    Currently, only supports Point geometry.
    """
    if s.crs != 4326:
        raise ValueError(f"Only support 'EPSG:4326' CRS, but got {s.crs!r}.")

    if isinstance(other, BaseGeometry):
        arr = np.empty(s.size, dtype=object)
        with catch_warnings():
            filterwarnings("ignore")
            arr[:] = other

    elif isinstance(other, gpd.base.GeoPandasBase):
        s = s.geometry
        if align and not s.index.equals(other.index):
            warn("The indices are different.", stacklevel=find_stack_level())
            s, other = s.align(other)
        else:
            other = other.geometry

    else:
        raise TypeError(f"Unknown type: {type(other)!r}.")

    return pd.Series(
        distance(
            s.geometry.x,
            s.geometry.y,
            other.geometry.x,
            other.geometry.y,
            radius=radius,
        ),
        index=s.index,
    )


# based on https://github.com/geopy/geopy geopy/distance.py::great_circle.measure
def distance(
    lng1: np.ndarray,
    lat1: np.ndarray,
    lng2: np.ndarray,
    lat2: np.ndarray,
    radius: float,
) -> np.ndarray:
    """
    The geodesic distance is the shortest distance on the surface of an ellipsoidal
    model of the earth. The default algorithm uses the method is given by
    `Karney (2013) <https://doi.org/10.1007%2Fs00190-012-0578-z>`_; this is accurate
    to round-off and always converges.
    """

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
