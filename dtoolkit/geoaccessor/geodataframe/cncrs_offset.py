import geopandas as gpd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.geoseries import cncrs_offset as s_cncrs_offset
from dtoolkit.geoaccessor.geoseries.cncrs_offset import CHINA_CRS
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
@doc(s_cncrs_offset, klass="GeoDataFrame")
def cncrs_offset(
    df: gpd.GeoDataFrame,
    /,
    from_crs: CHINA_CRS,
    to_crs: CHINA_CRS,
) -> gpd.GeoDataFrame:

    return df.assign(
        **{
            df.geometry.name: s_cncrs_offset(
                df.geometry,
                from_crs=from_crs,
                to_crs=to_crs,
            ),
        }
    )
