from __future__ import annotations

from textwrap import dedent
from typing import TYPE_CHECKING

import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.geoseries import count_coordinates as s_count_coordinates
from dtoolkit.geoaccessor.geoseries import geobuffer as s_geobuffer
from dtoolkit.geoaccessor.geoseries import get_coordinates as s_get_coordinates
from dtoolkit.geoaccessor.geoseries import utm_crs as s_utm_crs
from dtoolkit.geoaccessor.register import register_geodataframe_method

if TYPE_CHECKING:
    from dtoolkit._typing import OneDimArray


@register_geodataframe_method
@doc(
    s_geobuffer,
    klass=":class:`~geopandas.GeoDataFrame`",
    alias="df",
    examples=dedent(
        """
    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd
    >>> df = (
    ...      pd.DataFrame(
    ...          {
    ...              "where": ["close to equator", "away from equator"],
    ...              "x": [122, 100],
    ...              "y": [55, 1],
    ...          },
    ...      )
    ...      .points_from_xy(
    ...          "x",
    ...          "y",
    ...          crs=4326,
    ...          drop=True,
    ...     )
    ... )
    >>> df
                   where                    geometry
    0   close to equator  POINT (122.00000 55.00000)
    1  away from equator   POINT (100.00000 1.00000)
    >>> df.geobuffer(100)
                   where                                           geometry
    0   close to equator  POLYGON ((122.00156 55.00001, 122.00156 54.999...
    1  away from equator  POLYGON ((100.00090 1.00000, 100.00089 0.99991...
    """,
    ),
)
def geobuffer(
    df: gpd.GeoDataFrame,
    distance: int | float | list[int | float] | OneDimArray,
    **kwargs,
) -> gpd.GeoDataFrame:
    return df.assign(geometry=df.geometry.geobuffer(distance, **kwargs))


@register_geodataframe_method
@doc(
    s_count_coordinates,
    klass=":class:`~geopandas.GeoDataFrame`",
    examples=dedent(
        """
    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import geopandas as gpd
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
    s_get_coordinates,
    klass=":class:`~geopandas.GeoDataFrame`",
    examples=dedent(
        """
    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import geopandas as gpd
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


@register_geodataframe_method
@doc(s_utm_crs)
def utm_crs(df: gpd.GeoDataFrame, datum_name: str = "WGS 84") -> pd.Series:
    return df.geometry.utm_crs(datum_name=datum_name)
