from __future__ import annotations

from typing import Hashable

import geopandas as gpd
import pandas as pd

from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
def polygons_to_h3(
    s: gpd.GeoSeries,
    /,
    resolution: int,
    column: Hashable = "h3",
    drop: bool = True,
) -> pd.Series | gpd.GeoDataFrame:
    # TODO: Use `polygon_to_cells` instead of `polyfill`
    # While h3-py release 4, `polygon_to_cells` is not available.

    # requires h3 >= 4
    # from h3.api.numpy_int import polygon_to_cells
    # requires h3 < 4
    from h3.api.numpy_int import polyfill

    if not all(s.geom_type == "Polygon"):
        raise TypeError("Only support 'Polygon' geometry type.")
    if s.crs != 4326:
        raise ValueError(f"Only support 'EPSG:4326' CRS, but got {s.crs!r}.")
    if not drop and (column is None or s.name is None):
        raise ValueError(
            "to keep the original data requires setting the 'name' of "
            f"{s.__class__.__name__!r} and 'column'.",
        )

    h3_list = s.apply(
        lambda geom: polyfill(
            geom.__geo_interface__,
            resolution,
            geo_json_conformant=True,
        )
    )
    h3 = h3_list.explode().rename(s.name or column)

    return h3 if drop else pd.concat((s.repeat(s_len(h3_list)), h3), axis=1)
