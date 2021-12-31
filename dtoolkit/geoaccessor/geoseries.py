from __future__ import annotations

from textwrap import dedent
from typing import TYPE_CHECKING

import geopandas as gpd
import numpy as np
import pandas as pd
import pygeos
from pandas.util._decorators import doc

from dtoolkit.accessor.series import get_attr  # noqa
from dtoolkit.geoaccessor.register import register_geoseries_method

if TYPE_CHECKING:
    from dtoolkit._typing import OneDimArray


@register_geoseries_method
@doc(
    klass=":class:`~geopandas.GeoSeries`",
    alias="s",
    examples=dedent(
        """
    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import geopandas as gpd
    >>> from shapely.geometry import Point, LineString
    >>> s = gpd.GeoSeries(
    ...     [
    ...         Point(122, 55),
    ...         Point(100, 1),
    ...         LineString([Point(122, 55), Point(100, 1)])
    ...     ],
    ...     crs="EPSG:4326",
    ... )
    >>> s
    0    POINT (122.00000 55.00000)
    1    POINT (100.00000  1.00000)
    2    LINESTRING (122.00000 55.00000, 100.00000 1.00...
    dtype: geometry
    >>> s.geobuffer(100)
    0    POLYGON ((122.00156 55.00001, 122.00156 54.999...
    1    POLYGON ((100.00090 1.00000, 100.00089 0.99991...
    2    POLYGON ((100.00088 0.99981, 100.00086 0.99972...
    dtype: geometry
    """,
    ),
)
def geobuffer(
    s: gpd.GeoSeries,
    distance: int | float | list[int | float] | OneDimArray,
    **kwargs,
) -> gpd.GeoSeries:
    """
    Creates geographic buffers for {klass}.

    Reprojects input features into the *UTM* projection, buffers them,
    then reprojects back into the original geographic coordinates.

    Parameters
    ----------
    distance : int, float, list-like of int or float, the unit is meter.
        The radius of the buffer. If :obj:`~numpy.ndarray` or :obj:`~pandas.Series`
        are used then it must have same length as the ``{alias}``.

    Returns
    -------
    {klass}

    See Also
    --------
    dtoolkit.geoaccessor.geoseries.geobuffer
    dtoolkit.geoaccessor.geodataframe.geobuffer
    geopandas.GeoSeries.buffer

    {examples}
    """
    from pandas.api.types import is_list_like
    from pandas.api.types import is_number

    if is_list_like(distance):
        if len(distance) != len(s):
            raise IndexError(
                f"Length of 'distance' doesn't match length of the {type(s)!r}.",
            )

        if isinstance(distance, pd.Series):
            if not s.index.equals(distance.index):
                raise IndexError(
                    "Index values of 'distance' sequence doesn't "
                    f"match index values of the {type(s)!r}",
                )
        else:
            distance = np.asarray(distance)

    elif not is_number(distance):
        raise TypeError("type of 'distance' should be int or float.")

    utms = s.utm_crs().get_attr("code").to_numpy()

    s_index = s.index
    s = s.reset_index(drop=True)
    return (
        pd.concat(
            (
                s[utms == utm]
                .to_crs(epsg=utm)
                .buffer(
                    distance[utms == utm] if is_list_like(distance) else distance,
                    **kwargs,
                )
                .to_crs(s.crs)
            )
            if utm is not None
            else s[utms == utm]
            for utm in np.unique(utms)
        )
        .sort_index()
        .set_axis(s_index)
        .rename(s.name)
        .set_crs(s.crs)
    )


@register_geoseries_method
@doc(
    klass=":class:`~geopandas.GeoSeries`",
    examples=dedent(
        """
    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import geopandas as gpd
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

    return s.apply(
        lambda x: pygeos.count_coordinates(
            pygeos.from_shapely(x),
        ),
    )


@register_geoseries_method
@doc(
    klass=":class:`~geopandas.GeoSeries`",
    examples=dedent(
        """
    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import geopandas as gpd
    >>> s = gpd.GeoSeries.from_wkt(["POINT (0 0)", "LINESTRING (2 2, 4 4)", None])
    >>> s
    0                          POINT (0.00000 0.00000)
    1    LINESTRING (2.00000 2.00000, 4.00000 4.00000)
    2                                             None
    dtype: geometry
    >>> s.get_coordinates()
    0                [[0.0, 0.0]]
    1    [[2.0, 2.0], [4.0, 4.0]]
    2                          []
    dtype: object
    """,
    ),
)
def get_coordinates(
    s: gpd.GeoSeries,
    include_z: bool = False,
    return_index: bool = False,
) -> pd.Series:
    """
    Gets coordinates from each geometry of {klass}.

    Parameters
    ----------
    include_zbool: bool, default False
        If True include the third dimension in the output.
        If geometry has no third dimension, the z-coordinates will be `NaN`.

    return_index: bool, default False
        If True also return the index of each returned geometry.
        For multidimensional, this indexes into the flattened array
        (in C contiguous order).

    Returns
    -------
    Series

    See Also
    --------
    dtoolkit.geoaccessor.geoseries.get_coordinates
        Gets coordinates from each geometry of GeoSeries.
    dtoolkit.geoaccessor.geodataframe.get_coordinates
        Gets coordinates from each geometry of GeoDataFrame.
    pygeos.coordinates.get_coordinates
        The core algorithm of this accessor.
    {examples}
    """

    return s.apply(
        lambda x: pygeos.get_coordinates(
            pygeos.from_shapely(x),
            include_z=include_z,
            return_index=return_index,
        ),
    )


@register_geoseries_method
def utm_crs(s: gpd.GeoSeries, datum_name: str = "WGS 84") -> pd.Series:
    """
    Returns the estimated UTM CRS based on the bounds of each geometry.

    Parameters
    ----------
    datum_name : str, default 'WGS 84'
        The name of the datum in the CRS name ('NAD27', 'NAD83', 'WGS 84', …).

    Returns
    -------
    Series
        The element type is :class:`~pyproj.database.CRSInfo`.

    See Also
    --------
    dtoolkit.geoaccessor.geoseries.utm_crs
        Returns the estimated UTM CRS based on the bounds of each geometry.
    dtoolkit.geoaccessor.geodataframe.utm_crs
        Returns the estimated UTM CRS based on the bounds of each geometry.
    geopandas.GeoSeries.estimate_utm_crs
        Returns the estimated UTM CRS based on the bounds of the dataset.
    geopandas.GeoDataFrame.estimate_utm_crs
        Returns the estimated UTM CRS based on the bounds of the dataset.

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import dtoolkit.geoaccessor
    >>> import geopandas as gpd
    >>> s = gpd.GeoSeries.from_wkt(["Point (120 50)", "Point (100 1)"], crs="epsg:4326")
    >>> s.utm_crs()
    0    (EPSG, 32650, WGS 84 / UTM zone 50N, PJType.PR...
    1    (EPSG, 32647, WGS 84 / UTM zone 47N, PJType.PR...
    dtype: object

    Same operate for GeoDataFrame.

    >>> s.to_frame("geometry").utm_crs()
    0    (EPSG, 32650, WGS 84 / UTM zone 50N, PJType.PR...
    1    (EPSG, 32647, WGS 84 / UTM zone 47N, PJType.PR...
    dtype: object

    Get the EPSG code.

    >>> s.utm_crs().get_attr("code")
    0    32650
    1    32647
    dtype: object
    """

    from pyproj.aoi import AreaOfInterest
    from pyproj.database import query_utm_crs_info

    return s.bounds.apply(
        lambda bound: query_utm_crs_info(
            datum_name=datum_name,
            area_of_interest=AreaOfInterest(
                west_lon_degree=bound["minx"],
                south_lat_degree=bound["miny"],
                east_lon_degree=bound["maxx"],
                north_lat_degree=bound["maxy"],
            ),
        )[0]
        if not bound.isna().all()
        else None,
        axis=1,
    )
