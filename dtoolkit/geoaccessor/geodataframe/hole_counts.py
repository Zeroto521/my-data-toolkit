import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.geoseries import hole_counts as s_hole_counts
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
@doc(s_hole_counts, alias="df")
def hole_counts(df: gpd.GeoDataFrame, /) -> pd.Series:
    return s_hole_counts(df.geometry)
