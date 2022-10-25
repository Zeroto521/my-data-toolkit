import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.geoseries import geoarea as s_geoarea
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
@doc(s_geoarea, alias="df")
def geoarea(df: gpd.GeoDataFrame, /) -> pd.Series:

    return s_geoarea(df.geometry)
