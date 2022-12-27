import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.geodataframe import drop_geometry
from dtoolkit.geoaccessor.geoseries import reverse_geocode as s_reverse_geocode
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
@doc(s_reverse_geocode, klass="GeoDataFrame")
def reverse_geocode(
    df: gpd.GeoDataFrame,
    /,
    provider: str | "geopy.geocoder" = "photon",
    address: Hashable = "address",
    min_delay_seconds: float = 0,
    max_retries: int = 2,
    error_wait_seconds: float = 5,
    **kwargs,
) -> gpd.GeoDataFrame:

    return pd.concat(
        (
            drop_geometry(df),
            s_reverse_geocode(
                df.geometry,
                provider=provider,
                address=address,
                min_delay_seconds=min_delay_seconds,
                max_retries=max_retries,
                error_wait_seconds=error_wait_seconds,
                **kwargs,
            ),
        ),
        axis=1,
    ).to_geoframe()
