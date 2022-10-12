from __future__ import annotations

from typing import Hashable

import geopandas as gpd
import pandas as pd

from dtoolkit.geoaccessor.geoseries.xy import xy
from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
def xy_to_h3(
    s: gpd.GeoSeries,
    /,
    resolution: int,
    column: Hashable = None,
    drop: bool = True,
) -> pd.Series | gpd.GeoDataFrame:
    """
    Convert Point to containing H3 cell index.

    Parameters
    ----------
    resolution : int
        H3 resolution.

    column : Hashable, default None
        Name of the column to store the H3 cell index.

    drop : bool, default True
        Whether to drop the geometry column.

    Returns
    -------
    Series or GeoDataFrame
        Series if drop is True else GeoDataFrame.

    See Also
    --------
    h3.geo_to_h3
        https://h3geo.org/docs/api/indexing#latlngtocell

    dtoolkit.geoaccessor.geoseries.xy_to_h3
    """

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
    h3 = xy(s, reverse=True).apply(func).rename(column)

    return h3 if drop else pd.concat((s, h3))
