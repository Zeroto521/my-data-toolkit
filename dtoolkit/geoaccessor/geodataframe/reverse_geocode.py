import geopandas as gpd
import pandas as pd

from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
def reverse_geocode(df: gpd.GeoDataFrame, **kwargs) -> gpd.GeoDataFrame:

    return gpd.tools.reverse_geocode(df.geometry, **kwargs)
