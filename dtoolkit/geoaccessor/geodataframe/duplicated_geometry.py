import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.geoseries import duplicated_geometry as s_duplicated_geometry
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
@doc(s_duplicated_geometry)
def duplicated_geometry(df: gpd.GeoDataFrame, /, **kwargs) -> pd.Series:
    return df.geometry.duplicated_geometry(**kwargs)
