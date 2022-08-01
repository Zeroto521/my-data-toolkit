import pandas as pd
import geopandas as gpd
from pandas.util._decorators import doc


from dtoolkit.geoaccessor.geoseries import (
    duplicated_geometry_groups as s_duplicated_geometry_groups,
)
from dtoolkit.geoaccessor.geoseries.duplicated_geometry_groups import BINARY_PREDICATE

from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
@doc(s_duplicated_geometry_groups)
def duplicated_geometry_groups(
    df: gpd.GeoDataFrame,
    /,
    predicate: BINARY_PREDICATE = "intersects",
) -> pd.Series:
    return df.geometry.duplicated_geometry_groups(predicate=predicate)