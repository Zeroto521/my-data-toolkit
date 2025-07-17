from __future__ import annotations

from typing import Hashable
from typing import TYPE_CHECKING

import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.accessor.register import register_dataframe_method
from dtoolkit.geoaccessor.series import geocode as s_geocode


if TYPE_CHECKING:
    import geopy.geocoders


@register_dataframe_method
@doc(s_geocode)
def geocode(
    df: pd.DataFrame,
    /,
    address: Hashable = "address",
    provider: str | geopy.geocoder = "photon",
    min_delay_seconds: float = 0,
    max_retries: int = 2,
    error_wait_seconds: float = 5,
    **kwargs,
) -> gpd.GeoDataFrame:
    return pd.concat(
        (
            df.drop(columns=address),
            s_geocode(
                df[address],
                provider=provider,
                min_delay_seconds=min_delay_seconds,
                max_retries=max_retries,
                error_wait_seconds=error_wait_seconds,
                **kwargs,
            ),
        ),
        axis=1,
    ).to_geoframe()
