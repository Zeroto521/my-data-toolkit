from __future__ import annotations

import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc
from pyproj import CRS

from dtoolkit._typing import OneDimArray
from dtoolkit.geoaccessor._util import is_int_or_float
from dtoolkit.geoaccessor._util import string_or_int_to_crs
from dtoolkit.geoaccessor.register import register_geoseries_method
from dtoolkit.geoaccessor.tool import geographic_buffer


@register_geoseries_method
@doc(klass="GeoSeries")
def geobuffer(
    df: gpd.GeoSeries,
    distance: int | float | OneDimArray,
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
    df : {klass}
        Only support `Point` geometry, at present.

    distance : int, float, ndarray or Series, the unit is meter.
        The radius of the buffer. If :obj:`~numpy.ndarray` or
        :obj:`~pandas.Series` are used then it must have same length as the
        :obj:`~geopandas.GeoSeries`.

    crs : str, optional
        If ``epsg`` is specified, the value can be anything accepted by
        :meth:`~pyproj.crs.CRS.from_user_input`, such as an authority string
        (e.g. "EPSG:4326") or a WKT string.

    epsg : int, optional

        * If ``df.crs`` is not None, the result would use the CRS of
          :obj:`~geopandas.GeoSeries`.
        * If ``df.crs`` is None, the result would use the CRS from ``crs`` or
          ``epsg``.
        * If ``crs`` is specified EPSG code specifying output projection.
        * If ``df.crs`` is ``None``, the result would use `EPSG:4326`

    Returns
    -------
    {klass}

    See Also
    --------
    dtoolkit.geoaccessor.tool.geographic_buffer : The core algorithm for creating
        geographic buffer.
    shapely.geometry.base.BaseGeometry.buffer
        https://shapely.readthedocs.io/en/latest/manual.html#object.buffer
    """

    if isinstance(distance, pd.Series) and not df.index.equals(distance.index):
        raise IndexError(
            "Index values of distance sequence does "
            "not match index values of the GeoSeries",
        )

    crs: CRS = df.crs or string_or_int_to_crs(crs, epsg)

    if is_int_or_float(distance):
        result = df.apply(
            geographic_buffer,
            distance=distance,
            crs=crs,
            **kwargs,
        )
    elif len(distance) != len(df):
        raise IndexError(
            f"Length of 'distance' doesn't match length of the {type(df)!r}.",
        )
    else:
        result = (
            geographic_buffer(geom, distance=dist, crs=crs, **kwargs)
            for geom, dist in zip(df.geometry, distance)
        )

    return gpd.GeoSeries(result, crs=crs)
