import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.geoseries import (
    count_duplicated_geometry as s_count_duplicated_geometry,
)
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
@doc(s_count_duplicated_geometry, klass=":class:`~geopandas.GeoDataFrame`")
def count_duplicated_geometry(df: gpd.GeoDataFrame, /, **kwargs) -> pd.Series:
    return df.geometry.count_duplicated_geometry(**kwargs)