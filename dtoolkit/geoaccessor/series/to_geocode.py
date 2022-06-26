import pandas as pd
import geopandas as gpd

from dtoolkit.accessor.register import register_series_method


@register_series_method
def to_geocode(s: pd.Series, drop: bool = False) -> gpd.GeoDataFrame:
    if s.name is None and not drop:
        raise ValueError("")

    df = gpd.tools.geocode(s)
    return df if drop else pd.concat((s, df), axis=1)
