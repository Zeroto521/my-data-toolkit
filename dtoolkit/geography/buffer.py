from __future__ import annotations

from warnings import warn

import geopandas as gpd
import numpy as np
import pandas as pd
from pyproj import CRS
from pyproj import Transformer
from pyproj.crs import ProjectedCRS
from pyproj.crs.coordinate_operation import AzumuthalEquidistantConversion
from shapely.geometry import Point
from shapely.geometry.base import BaseGeometry
from shapely.ops import transform

from .._checking import bad_condition_raise_error
from .._checking import check_geometry_type
from .._checking import check_geopandas_type
from .._checking import check_greater_than_zero
from .._checking import check_number_tyep
from .._checking import istype
from .._typing import GPd
from .._typing import Num
from .._typing import NumericTypeList


def geographic_buffer(
    df: GPd,
    distance: Num | list[Num] | np.ndarray | pd.Series,
    crs: str | None = None,
    epsg: int | None = None,
    **kwargs,
) -> gpd.GeoSeries:
    """
    Creates a geographic buffer.

    Creates a buffer zone of specified size around or inside geometry. It
    is designed for use with features in Geographic coordinates. Reprojects
    input features into the DynamicEqual Distance projection, buffers them,
    then reprojects back into the original Geographic coordinates.

    Parameters
    ----------
    df : GeoSeries
        Only support `Point` geometry, at present. If
        [geopandas#1952](https://github.com/geopandas/geopandas/pull/1952)
        done, this method would be a :obj:`~geopandas.GeoSeries` or
        :obj:`~geopandas.GeoDataFrame` and be easier to use.

    distance : int, float, ndarray or Series, the unit is meter.
        The radius of the buffer. If :obj:`~numpy.ndarray` or
        :obj:`~pandas.Series` are used then it must have same length as the
        :obj:`~geopandas.GeoSeries`.

    crs : str, optional
        If ``epsg`` is specified, the value can be anything accepted by
        :meth:`~pyproj.CRS.from_user_input`, such as an authority string
        (eg "EPSG:4326") or a WKT string.

    epsg : int, optional
        * If ``df.crs`` is not None, the result would use the :obj:`~geopandas.GeoSeries` crs.
        * If ``df.crs`` is None, the result would use the crs from ``crs`` or ``epsg``.
        * If ``crs`` is specified EPSG code specifying output projection.
        * If ``df.crs`` is ``None``, the result would use `EPSG:4326`

    Returns
    -------
    GeoSeries
        A ``GeoSeries`` of geometries representing all points within a given
        ``distance`` of each geometric object.

    See Also
    --------
    shapely.geometry.base.BaseGeometry.buffer
        https://shapely.readthedocs.io/en/latest/manual.html#object.buffer
    """

    check_geopandas_type(df)

    if istype(distance, pd.Series) and not df.index.equals(distance.index):
        raise IndexError(
            "Index values of distance sequence does "
            "not match index values of the GeoSeries",
        )

    if not istype(distance, NumericTypeList):
        distance = np.asarray(distance)

    gscrs: CRS = df.crs or string_or_int_to_crs(crs, epsg)

    out: np.ndarray = np.empty(len(df), dtype=object)
    if istype(distance, np.ndarray):
        bad_condition_raise_error(
            len(distance) != len(df),
            IndexError,
            "Length of distance doesn't match length of the GeoSeries.",
        )

        out[:] = [
            _geographic_buffer(geom, distance=dist, crs=gscrs, **kwargs)
            for geom, dist in zip(df.geometry, distance)
        ]
    else:
        out[:] = [
            _geographic_buffer(geom, distance, crs=gscrs, **kwargs)
            for geom in df.geometry
        ]

    return gpd.GeoSeries(out, crs=gscrs)


def string_or_int_to_crs(
    crs: str | None = None,
    epsg: int | None = None,
) -> CRS:
    if crs is not None:
        return CRS.from_user_input(crs)
    elif epsg is not None:
        return CRS.from_epsg(epsg)

    warn(
        "The crs is missing, and the crs would be set 'EPSG:4326'.",
        UserWarning,
    )
    return CRS.from_epsg(4326)


def _geographic_buffer(
    geom: BaseGeometry | None,
    distance: Num,
    crs: CRS | None = None,
    **kwargs,
) -> BaseGeometry | None:

    if geom is None:
        return None

    check_geometry_type(geom)

    check_number_tyep(distance)
    check_greater_than_zero(distance)

    crs = crs or string_or_int_to_crs()

    azmed = ProjectedCRS(AzumuthalEquidistantConversion(geom.y, geom.x))
    project: Transformer = Transformer.from_proj(azmed, crs, always_xy=True)

    p: BaseGeometry = Point(0, 0)  # TODO: extend to other geometry
    buffer: BaseGeometry = p.buffer(distance, **kwargs)
    return transform(project.transform, buffer)
