import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.geodataframe import drop_geometry
from dtoolkit.geoaccessor.geoseries import reverse_geocode as s_reverse_geocode
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
@doc(s_reverse_geocode, klass="GeoDataFrame")
def reverse_geocode(df: gpd.GeoDataFrame, /, **kwargs) -> gpd.GeoDataFrame:

    return pd.concat(
        (
            s_reverse_geocode(df.geometry, **kwargs),
            drop_geometry(df),
        ),
        axis=1,
    )
