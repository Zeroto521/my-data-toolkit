from __future__ import annotations

from typing import Optional
from warnings import warn

import geopandas as gpd
import numpy as np
import pandas as pd
from pyproj import CRS, Transformer
from pyproj.crs import ProjectedCRS
from pyproj.crs.coordinate_operation import AzumuthalEquidistantConversion
from shapely.geometry import Point
from shapely.geometry.base import BaseGeometry
from shapely.ops import transform

from ._typing import Num, NumericTypeList


def geographic_buffer(
    data: gpd.GeoSeries,
    distance: Num | list[Num] | np.ndarray | pd.Series,
    resolution: int = 16,
    crs: Optional[str] = None,
    epsg: Optional[int] = None,
    **kwargs,
) -> gpd.GeoSeries:
    """
    Creates a buffer zone of specified size around or inside geometry.
    Works similarly to the Bufferer, but is designed for use with
    features in Geographic coordinates. Reprojects input features into
    the DynamicEqual Distance projection, buffers them,
    then reprojects back into the original Geographic coordinates.

    Returns a ``GeoSeries`` of geometries representing all points within
    a given ``distance`` of each geometric object.

    See http://shapely.readthedocs.io/en/latest/manual.html#object.buffer
    for details.

    Parameters
    ----------
    data : gpd.GeoSeries
        Only support `Point` geometry, at present.
        if [geopandas#1952](https://github.com/geopandas/geopandas/pull/1952)
        done, this method would be a `accessor` and be easier to use.
    distance : int, float, np.ndarray, pd.Series, the unit is meter.
        The radius of the buffer. If `np.ndarray` or `pd.Series` are used
        then it must have same length as the GeoSeries.
    resolution : int, optional, default 16
        The resolution of the buffer around each vertex.
    crs : str, optional
        if `epsg` is specified The value can be anything accepted by
        :meth:`pyproj.CRS.from_user_input() <pyproj.crs.CRS.from_user_input>`,
        such as an authority string (eg "EPSG:4326") or a WKT string.
    epsg : int, optional
        If `data.crs` is not None, the result would use the `GeoSeries` crs.
        If `data.crs` is None, the result would use
        the crs from `crs` or `epsg`.
        If `crs` is specified EPSG code specifying output projection.
        If `data` crs is `None`, the result would use `EPSG:4326`
    """

    if isinstance(distance, pd.Series):  # sourcery skip
        if not data.index.equals(distance.index):
            raise IndexError(
                "Index values of distance sequence does "
                "not match index values of the GeoSeries"
            )

    if not isinstance(distance, tuple(NumericTypeList)):
        distance = np.asarray(distance)

    gscrs: CRS = data.crs or string_or_int_to_crs(crs, epsg)

    out: np.ndarray = np.empty(len(data), dtype=object)
    if isinstance(distance, np.ndarray):
        if len(distance) != len(data):
            raise IndexError(
                "Length of distance sequence does not"
                + "match length of the GeoSeries."
            )

        out[:] = [
            _geographic_buffer(
                geom, distance=dist, crs=gscrs, resolution=resolution, **kwargs
            )
            for geom, dist in zip(data, distance)
        ]
    else:
        out[:] = [
            _geographic_buffer(
                geom, distance, crs=gscrs, resolution=resolution, **kwargs
            )
            for geom in data
        ]

    return gpd.GeoSeries(out, crs=gscrs)


def string_or_int_to_crs(
    crs: Optional[str] = None,
    epsg: Optional[int] = None,
) -> CRS:
    if crs is not None:
        return CRS.from_user_input(crs)
    elif epsg is not None:
        return CRS.from_epsg(epsg)
    else:
        warn(
            "The crs is missing, and the crs would be set 'EPSG:4326'.",
            UserWarning,
        )
        return CRS.from_epsg(4326)


def _geographic_buffer(
    geom: Optional[BaseGeometry],
    distance: Num,
    crs: Optional[CRS] = None,
    resolution: int = 16,
    **kwargs,
) -> Optional[BaseGeometry]:

    if geom is None:
        return None

    if not isinstance(distance, tuple(NumericTypeList)):
        raise TypeError("The type of distance must be int or float.")

    if distance <= 0:
        raise ValueError("The distance must be greater than 0.")

    crs = crs or string_or_int_to_crs()

    azmed = ProjectedCRS(AzumuthalEquidistantConversion(geom.y, geom.x))
    project: Transformer = Transformer.from_proj(azmed, crs, always_xy=True)

    # TODO: extend to other geometry
    p: BaseGeometry = Point(0, 0)
    buffer: BaseGeometry = p.buffer(distance, resolution=resolution, **kwargs)
    return transform(project.transform, buffer)
