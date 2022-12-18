import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.geoseries import coordinates as s_coordinates
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method("get_coordinates")
@register_geodataframe_method
@doc(s_coordinates, klass="GeoDataFrame")
def coordinates(df: gpd.GeoDataFrame, /, **kwargs) -> pd.Series:
    return s_coordinates(df.geometry, **kwargs)
