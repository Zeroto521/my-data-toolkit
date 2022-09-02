import geopandas as gpd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.geoseries import bd09_to_gcj02 as s_bd09_to_gcj02
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
@doc(s_bd09_to_gcj02, klass="GeoDataFrame")
def bd09_to_gcj02(df: gpd.GeoDataFrame, /) -> gpd.GeoDataFrame:
    return s_bd09_to_gcj02(df.geometry)
