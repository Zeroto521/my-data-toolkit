from __future__ import annotations

from typing import Hashable

import geopandas as gpd
from pandas.util._decorators import doc

from dtoolkit._typing import Number
from dtoolkit._typing import OneDimArray
from dtoolkit.geoaccessor.geoseries import geobuffer as s_geobuffer
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
@doc(s_geobuffer, klass="GeoDataFrame", alias="df")
def geobuffer(
    df: gpd.GeoDataFrame,
    distance: Hashable | Number | list[Number] | OneDimArray,
    /,
    **kwargs,
) -> gpd.GeoDataFrame:

    # NOTE: Require pandas >= 1.3.0 to support `isinstance(SeriesOrDataFrame, Hashable)`
    if isinstance(distance, Hashable) and distance in df.columns:
        distance = df[distance]

    return df.assign(
        **{
            df.geometry.name: s_geobuffer(
                df.geometry,
                distance,
                **kwargs,
            ),
        }
    )
