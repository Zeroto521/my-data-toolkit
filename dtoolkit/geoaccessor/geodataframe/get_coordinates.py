import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.geoseries import get_coordinates as s_get_coordinates
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
@doc(s_get_coordinates, klass="GeoDataFrame")
def get_coordinates(df: gpd.GeoDataFrame, /, **kwargs) -> pd.Series:
    return s_get_coordinates(df.geometry, **kwargs)
