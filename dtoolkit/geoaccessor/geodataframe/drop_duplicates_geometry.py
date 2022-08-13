from typing import Literal

import geopandas as gpd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.geodataframe.duplicated_geometry import duplicated_geometry
from dtoolkit.geoaccessor.geoseries import (
    drop_duplicates_geometry as s_drop_duplicates_geometry,
)
from dtoolkit.geoaccessor.geoseries.duplicated_geometry_groups import BINARY_PREDICATE
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
@doc(s_drop_duplicates_geometry, klass="GeoDataFrame")
def drop_duplicates_geometry(
    df: gpd.GeoDataFrame,
    /,
    predicate: BINARY_PREDICATE = "intersects",
    keep: Literal["first", "last", False] = "first",
) -> gpd.GeoDataFrame:
    return df[~duplicated_geometry(df, predicate=predicate, keep=keep)]
