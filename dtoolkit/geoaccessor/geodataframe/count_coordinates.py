import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.geoseries import count_coordinates as s_count_coordinates
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
@doc(s_count_coordinates, klass="GeoDataFrame")
def count_coordinates(df: gpd.GeoDataFrame, /) -> pd.Series:
    return s_count_coordinates(df.geometry)
