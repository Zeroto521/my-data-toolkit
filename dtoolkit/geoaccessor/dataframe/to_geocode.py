from typing import Hashable

import geopandas as gpd
import pandas as pd

from dtoolkit.accessor.dataframe import drop_or_not  # noqa
from dtoolkit.accessor.register import register_dataframe_method


@register_dataframe_method
def to_geocode(
    df: pd.DataFrame,
    column: Hashable,
    drop: bool = False,
    **kwargs,
) -> gpd.GeoDataFrame:
    return pd.concat(
        (
            df.drop_or_not(drop=drop, columns=column),
            gpd.tools.geocode(df[column], **kwargs),
        ),
        axis=1,
    )
