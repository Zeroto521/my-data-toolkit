from __future__ import annotations

from typing import TYPE_CHECKING

import geopandas as gpd
import pandas as pd
from geopandas.base import is_geometry_type

from dtoolkit.accessor.register import register_series_method

if TYPE_CHECKING:
    from pyproj import CRS


@register_series_method
def to_geoseries(
    s: pd.Series,
    crs: CRS | str | int = None,
) -> gpd.GeoSeries | pd.Series:
    if is_geometry_type(s):
        s = gpd.GeoSeries(s)
        if crs:
            s = s.to_crs(crs) if s.crs else s.set_crs(crs)

    return s
