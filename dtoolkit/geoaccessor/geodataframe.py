from __future__ import annotations

import geopandas as gpd
from pandas.util._decorators import doc

from dtoolkit._typing import OneDimArray
from dtoolkit.geoaccessor.geoseries import geobuffer as geoseries_geobuffer  # noqa
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
