from __future__ import annotations

import geopandas as gpd
from pandas.util._decorators import doc

from dtoolkit._typing import Number
from dtoolkit._typing import OneDimArray
from dtoolkit.geoaccessor.geoseries import geobuffer as s_geobuffer
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
@doc(s_geobuffer, klass=":class:`~geopandas.GeoDataFrame`", alias="df")
def geobuffer(
    df: gpd.GeoDataFrame,
    distance: Number | list[Number] | OneDimArray,
    /,
    **kwargs,
) -> gpd.GeoDataFrame:

    return df.assign(
        **{
            df.geometry.name: s_geobuffer(
                df.geometry,
                distance,
                **kwargs,
            ),
        }
    )
