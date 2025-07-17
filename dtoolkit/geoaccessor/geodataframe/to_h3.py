import geopandas as gpd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.geoseries import to_h3 as s_to_h3
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
@doc(s_to_h3, klass="GeoDataFrame")
def to_h3(
    df: gpd.GeoDataFrame,
    /,
    resolution: int,
    int_dtype: bool = True,
) -> gpd.GeoDataFrame:

    return s_to_h3(df, resolution=resolution, int_dtype=int_dtype)
