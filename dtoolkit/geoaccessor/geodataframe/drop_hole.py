import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.geoseries import drop_hole as s_drop_hole
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
@doc(s_drop_hole, klass="GeoDataFrame", alias="df")
def drop_hole(df: gpd.GeoDataFrame, /) -> gpd.GeoDataFrame:

    return df.assign(**{df.geometry.name: s_drop_hole(df.geometry)})
