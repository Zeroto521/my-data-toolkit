import geopandas as gpd
import pandas as pd
from shapely.geometry.base import BaseGeometry

from dtoolkit.geoaccessor.geoseries import geoazimuth as s_geoazimuth
from dtoolkit.geoaccessor.register import register_geodataframe_method
from dtoolkit.util._decorator import doc


@register_geodataframe_method
@doc(s_geoazimuth)
def geoazimuth(
    df: gpd.GeoDataFrame,
    /,
    other: BaseGeometry | gpd.GeoSeries | gpd.GeoDataFrame,
    align: bool = True,
) -> pd.Series:
    return s_geoazimuth(df.geometry, other=other, align=align)
