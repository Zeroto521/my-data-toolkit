import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.geoseries import hole_count as s_hole_count
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
@doc(klass="df")
def hole_count(df: gpd.GeoDataFrame) -> pd.Series:
    return s_hole_count(df.geometry)
