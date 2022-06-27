import geopandas as gpd
import pandas as pd

from dtoolkit.accessor.dataframe import drop_or_not  # noqa
from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
def reverse_geocode(s: gpd.GeoSeries, **kwargs) -> gpd.GeoDataFrame:


    return gpd.tools.reverse_geocode(s.geometry, **kwargs)
