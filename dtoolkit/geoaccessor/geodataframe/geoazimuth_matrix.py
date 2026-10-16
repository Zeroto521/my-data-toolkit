import geopandas as gpd
import pandas as pd

from dtoolkit.geoaccessor.geoseries import geoazimuth_matrix as s_geoazimuth_matrix
from dtoolkit.geoaccessor.register import register_geodataframe_method
from dtoolkit.util._decorator import doc


@register_geodataframe_method
@doc(s_geoazimuth_matrix)
def geoazimuth_matrix(
    df: gpd.GeoDataFrame,
    /,
    other: gpd.GeoSeries | gpd.GeoDataFrame | None = None,
) -> pd.DataFrame:
    return s_geoazimuth_matrix(df.geometry, other=other)
