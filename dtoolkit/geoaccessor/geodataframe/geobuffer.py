from __future__ import annotations

from textwrap import dedent

import geopandas as gpd
from pandas.util._decorators import doc

from dtoolkit._typing import Number
from dtoolkit._typing import OneDimArray
from dtoolkit.geoaccessor.geoseries import geobuffer as s_geobuffer
from dtoolkit.geoaccessor.register import register_geodataframe_method


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
    distance: Number | list[Number] | OneDimArray,
    **kwargs,
) -> gpd.GeoDataFrame:

    return df.assign(
        geometry=df.geometry.geobuffer(
            distance,
            **kwargs,
        ),
    )
