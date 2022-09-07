from __future__ import annotations

import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc
from shapely.geometry.base import BaseGeometry

from dtoolkit.geoaccessor.geoseries import geodistance as s_geodistance
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
@doc(s_geodistance)
def geodistance(
    df: gpd.GeoDataFrame,
    /,
    other: BaseGeometry | gpd.GeoSeries | gpd.GeoDataFrame,
    align: bool = True,
    radius: float = 6371008.7714150598,
) -> pd.Series:

    return s_geodistance(df.geometry, other=other, align=align, radius=radius)
