from __future__ import annotations

import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.geoseries import geodistancey as s_geodistancey
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
@doc(s_geodistancey)
def geodistance(
    df: gpd.GeoDataFrame,
    /,
    other: BaseGeometry | gpd.GeoSeries | gpd.GeoDataFrame,
    align: bool = True,
    radius: float = 6371008.7714150598,
) -> pd.Series:

    return s_distance(df.geometry, Other=other, align=align, radius=radius)
