import geopandas as gpd
import pandas as pd

from dtoolkit.accessor.register import register_series_method


@register_series_method
def to_geocode(s: pd.Series, drop: bool = False, **kwargs) -> gpd.GeoDataFrame:
    if s.name is None and not drop:
        raise ValueError(
            "to keep the original data requires setting the 'name' of "
            f"{s.__class__.__name__!r}",
        )

    df = gpd.tools.geocode(s, **kwargs)
    return df if drop else pd.concat((s, df), axis=1)
