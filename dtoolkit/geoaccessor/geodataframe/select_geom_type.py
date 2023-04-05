import geopandas as gpd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.geoseries.select_geom_type import GEOM_TYPE
from dtoolkit.geoaccessor.geoseries.select_geom_type import (
    select_geom_type as s_select_geom_type,
)
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
@doc(klass="GeoDataFrame")
def select_geom_type(
    df: gpd.GeoDataFrame,
    geom_type: GEOM_TYPE,
    /,
    complement: bool = False,
) -> gpd.GeoDataFrame:

    return s_select_geom_type(df, geom_type, complement=complement)
