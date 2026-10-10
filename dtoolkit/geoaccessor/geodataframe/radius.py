import geopandas as gpd
import pandas as pd

from dtoolkit.geoaccessor.geoseries import radius as s_radius
from dtoolkit.geoaccessor.register import register_geodataframe_method
from dtoolkit.util._decorator import doc


@register_geodataframe_method
@doc(s_radius)
def radius(df: gpd.GeoDataFrame, /) -> pd.Series:
    return s_radius(df.geometry)
