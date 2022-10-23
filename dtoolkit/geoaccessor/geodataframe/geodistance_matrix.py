from __future__ import annotations

import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.geoseries import geodistance_matrix as s_geodistance_matrix
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
@doc(s_geodistance_matrix)
def geodistance_matrix(
    df: gpd.GeoDataFrame,
    /,
    other: gpd.GeoSeries | gpd.GeoDataFrame | None = None,
    radius: float = 6371008.7714150598,
) -> pd.DataFrame:

    return s_geodistance_matrix(df.geometry, other=other, radius=radius)
