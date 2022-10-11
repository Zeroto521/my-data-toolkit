import geopandas as gpd
import pandas as pd

from dtoolkit.geoaccessor.geoseries.xy import xy
from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
def xy_to_h3(s: gpd.GeoSeries, /, resolution: int) -> pd.Series:
    # TODO: Use `latlon_to_h3` instead of `geo_to_h3`
    # While h3-py release 4, `latlon_to_h3` is not available.

    # requires h3 >= 4
    # from h3.api.numpy_int import latlng_to_cell
    # requires h3 < 4

    # TODO: Advices for h3-pandas
    # 1. use `import h3.api.numpy_int as h3` instead of `import h3`
    # 2. compat with h3-py 4

    from h3.api.numpy_int import geo_to_h3

    if s.crs != 4326:
        raise ValueError(f"Only support 'EPSG:4326' CRS, but got {s.crs!r}.")

    func = lambda yx: geo_to_h3(*yx, resolution)
    return xy(s, reverse=True).apply(func)
