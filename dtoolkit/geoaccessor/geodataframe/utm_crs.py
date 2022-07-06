from __future__ import annotations

import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor import register_geodataframe_method
from dtoolkit.geoaccessor.geoseries import utm_crs as s_utm_crs


@register_geodataframe_method
@doc(s_utm_crs)
def utm_crs(df: gpd.GeoDataFrame, datum_name: str = "WGS 84") -> pd.Series:
    return df.geometry.utm_crs(datum_name=datum_name)
