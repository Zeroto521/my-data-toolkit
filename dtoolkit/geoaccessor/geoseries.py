from __future__ import annotations

from textwrap import dedent

import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc
from pygeos import count_coordinates as pygeos_count_coordinates
from pygeos import from_shapely
from pyproj import CRS

from dtoolkit._typing import OneDimArray
from dtoolkit.geoaccessor._util import is_int_or_float
from dtoolkit.geoaccessor._util import string_or_int_to_crs
from dtoolkit.geoaccessor.register import register_geoseries_method
from dtoolkit.geoaccessor.tool import geographic_buffer


@register_geoseries_method
@doc(klass="GeoSeries", alias="s")
def geobuffer(
    s: gpd.GeoSeries,
    distance: int | float | list | OneDimArray,
    crs: str | None = None,
    epsg: int | None = None,
    **kwargs,
) -> gpd.GeoSeries:
    """
    Creates geographic buffers for {klass}.

    Creates a buffer zone of specified size around or inside geometry. It
    is designed for use with features in Geographic coordinates. Reprojects
    input features into the DynamicEqual Distance projection, buffers them,
    then reprojects back into the original Geographic coordinates.

    Parameters
    ----------
    {alias} : {klass}
        Only support `Point` geometry, at present.

    distance : int, float, ndarray or Series, the unit is meter.
        The radius of the buffer. If :obj:`~numpy.ndarray` or
        :obj:`~pandas.Series` are used then it must have same length as the
        ``{alias}``.

    crs : str, optional
        If ``epsg`` is specified, the value can be anything accepted by
        :meth:`~pyproj.crs.CRS.from_user_input`, such as an authority string
        (e.g. "EPSG:4326") or a WKT string.

    epsg : int, optional

        * If ``{alias}.crs`` is not None, the result would use the CRS of
          :obj:`~geopandas.GeoSeries`.
        * If ``{alias}.crs`` is None, the result would use the CRS from ``crs``
          or ``epsg``.
        * If ``crs`` is specified EPSG code specifying output projection.
        * If ``{alias}.crs`` is ``None``, the result would use `EPSG:4326`

    Returns
    -------
    {klass}

    See Also
    --------
    dtoolkit.geoaccessor.geoseries.geobuffer
        Creates geographic buffers for GeoSeries.
    dtoolkit.geoaccessor.geodataframe.geobuffer
        Creates geographic buffers for GeoDataFrame1.
    dtoolkit.geoaccessor.tool.geographic_buffer
        The core algorithm for creating geographic buffer.
    shapely.geometry.base.BaseGeometry.buffer
        https://shapely.readthedocs.io/en/latest/manual.html#object.buffer
    """

    if is_int_or_float(distance):
        result = (geographic_buffer(g, distance, crs=crs, **kwargs) for g in s)
    else:
        if len(distance) != len(s):
            raise IndexError(
                f"Length of 'distance' doesn't match length of the {type(s)!r}.",
            )
        if isinstance(distance, pd.Series) and not s.index.equals(distance.index):
            raise IndexError(
                "Index values of 'distance' sequence doesn't "
                f"match index values of the {type(s)!r}",
            )

        result = (
            geographic_buffer(g, d, crs=crs, **kwargs) for g, d in zip(s, distance)
        )

    crs: CRS = s.crs or string_or_int_to_crs(crs, epsg)
    return gpd.GeoSeries(result, crs=crs, index=s.index, name=s.name)


@register_geoseries_method
@doc(
    klass=":class:`~geopandas.GeoSeries`",
    examples=dedent(
        """
    Examples
    --------
    >>> import geopandas as gpd
    >>> from dtoolkit.geoaccessor.geoseries import count_coordinates
    >>> s = gpd.GeoSeries.from_wkt(["POINT (0 0)", "LINESTRING (2 2, 4 4)", None])
    >>> s
    0                          POINT (0.00000 0.00000)
    1    LINESTRING (2.00000 2.00000, 4.00000 4.00000)
    2                                             None
    dtype: geometry

    >>> s.count_coordinates()
    0    1
    1    2
    2    0
    dtype: int64
    """,
    ),
)
def count_coordinates(s: gpd.GeoSeries) -> pd.Series:
    """
    Counts the number of coordinate pairs in each geometry of {klass}.

    Returns
    -------
    Series

    See Also
    --------
    dtoolkit.geoaccessor.geoseries.count_coordinates
        Counts the number of coordinate pairs in each geometry of GeoSeries.
    dtoolkit.geoaccessor.geodataframe.count_coordinates
        Counts the number of coordinate pairs in each geometry of GeoDataFrame.
    pygeos.coordinates.count_coordinates
        The core algorithm of this accessor.
    {examples}
    """

    return s.apply(lambda x: pygeos_count_coordinates(from_shapely(x)))
