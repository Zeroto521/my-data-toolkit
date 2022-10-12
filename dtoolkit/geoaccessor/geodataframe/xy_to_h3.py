from __future__ import annotations

from typing import Hashable

import pandas as pd
import geopandas as gpd

from dtoolkit.geoaccessor.geodataframe.drop_geometry import drop_geometry
from dtoolkit.geoaccessor.geoseries import xy_to_h3 as s_xy_to_h3
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
def xy_to_h3(
    df: gpd.GeoDataFrame,
    /,
    resolution: int,
    column: Hashable = "h3",
    drop: bool = True,
) -> pd.DataFrame | gpd.GeoDataFrame:

    h3 = s_xy_to_h3(df.geometry, resolution, column=column, drop=True)

    if drop:
        df = drop_geometry(df)

    return df.assign(**{column: h3})
