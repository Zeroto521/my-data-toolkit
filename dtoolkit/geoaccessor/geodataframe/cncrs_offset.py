import geopandas as gpd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.geoseries import cncrs_offset as s_cncrs_offset
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
@doc(s_bd09_to_gcj02, klass="GeoDataFrame")
def cncrs_offset(df: gpd.GeoDataFrame, /) -> gpd.GeoDataFrame:

    return df.assign(**{df.geometry.name: s_cncrs_offset(df.geometry)})
