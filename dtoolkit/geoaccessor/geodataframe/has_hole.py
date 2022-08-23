import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.geoseries import has_hole as s_has_hole
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
@doc(s_has_hole)
def has_hole(df: gpd.GeoDataFrame, /) -> pd.Series:
    return s_has_hole(df.geometry)
