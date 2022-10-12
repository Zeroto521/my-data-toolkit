from __future__ import annotations

import geopandas as gpd
import numpy as np
import pandas as pd

from dtoolkit.accessor.register import register_series_method
from dtoolkit.geoaccessor.series.to_geoframe import to_geoframe


@register_series_method
def points_from_h3(
    s: pd.Series,
    /,
    drop: bool = False,
) -> gpd.GeoSeries | gpd.GeoDataFrame:
    # TODO: Use `cell_to_latlng` instead of `h3_to_geo`
    # While h3-py release 4, `latlon_to_h3` is not available.

    # requires h3 >= 4
    # from h3.api.numpy_int import cell_to_latlng
    # requires h3 < 4
    from h3.api.numpy_int import h3_to_geo
    # TODO: delete pygeos after shapely 2.x released
    from pygeos import points

    if not drop and s.name is None:
        raise ValueError(
            "to keep the original data requires setting the 'name' of "
            f"{s.__class__.__name__!r}.",
        )

    yx = np.asarray(s.apply(h3_to_geo).tolist())
    geometry = gpd.GeoSeries.from_xy(yx[:, 1], yx[:, 0], crs=4326)

    return geometry if drop else to_geoframe(s, geometry=geometry)
