from typing import Literal

import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.geoseries import duplicated_geometry as s_duplicated_geometry
from dtoolkit.geoaccessor.geoseries.duplicated_geometry_groups import BINARY_PREDICATE
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
@doc(s_duplicated_geometry)
def duplicated_geometry(
    df: gpd.GeoDataFrame,
    /,
    predicate: BINARY_PREDICATE = "intersects",
    keep: Literal["first", "last", False] = "first",
) -> pd.Series:
    return s_duplicated_geometry(df.geometry, predicate=predicate, keep=keep)
