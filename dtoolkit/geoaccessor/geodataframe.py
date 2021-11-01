from __future__ import annotations

from textwrap import dedent

import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc

from dtoolkit._typing import OneDimArray
from dtoolkit.geoaccessor.geoseries import (
    count_coordinates as geoseries_count_coordinates,
)
from dtoolkit.geoaccessor.geoseries import geobuffer as geoseries_geobuffer
from dtoolkit.geoaccessor.geoseries import (
    get_coordinates as geoseries_get_coordinates,
)
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
@doc(geoseries_geobuffer, klass="GeoDataFrame", alias="df")
def geobuffer(
    df: gpd.GeoDataFrame,
    distance: int | float | OneDimArray,
    crs: str | None = None,
    epsg: int | None = None,
    **kwargs,
) -> gpd.GeoDataFrame:
    buffer = df.geometry.geobuffer(distance, crs=crs, epsg=epsg, **kwargs)
    return df.assign(geometry=buffer)


@register_geodataframe_method
@doc(
    geoseries_count_coordinates,
    klass=":class:`~geopandas.GeoDataFrame`",
    examples=dedent(
        """
    Examples
    --------
    >>> import geopandas as gpd
    >>> from dtoolkit.geoaccessor.geoseries import count_coordinates
    >>> d = gpd.GeoSeries.from_wkt(["POINT (0 0)", "LINESTRING (2 2, 4 4)", None])
    >>> d = d.to_frame("geometry")
    >>> d
                                            geometry
    0                        POINT (0.00000 0.00000)
    1  LINESTRING (2.00000 2.00000, 4.00000 4.00000)
    2                                           None
    >>> d.count_coordinates()
    0    1
    1    2
    2    0
    Name: geometry, dtype: int64
    """,
    ),
)
def count_coordinates(df: gpd.GeoDataFrame) -> pd.Series:
    return df.geometry.count_coordinates()


@register_geodataframe_method
@doc(
    geoseries_get_coordinates,
    klass=":class:`~geopandas.GeoDataFrame`",
    examples=dedent(
        """
    Examples
    --------
    >>> import geopandas as gpd
    >>> from dtoolkit.geoaccessor.geodataframe import get_coordinates
    >>> d = gpd.GeoSeries.from_wkt(["POINT (0 0)", "LINESTRING (2 2, 4 4)", None])
    >>> d = d.to_frame("geometry")
    >>> d
                                            geometry
    0                        POINT (0.00000 0.00000)
    1  LINESTRING (2.00000 2.00000, 4.00000 4.00000)
    2                                           None

    >>> d.get_coordinates()
    0                [[0.0, 0.0]]
    1    [[2.0, 2.0], [4.0, 4.0]]
    2                          []
    Name: geometry, dtype: object
    """,
    ),
)
def get_coordinates(
    df: gpd.GeoDataFrame,
    include_z: bool = False,
    return_index: bool = False,
) -> pd.Series:

    return df.geometry.get_coordinates(
        include_z=include_z,
        return_index=return_index,
    )
