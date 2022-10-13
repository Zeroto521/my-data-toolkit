from __future__ import annotations

import geopandas as gpd
import numpy as np
import pandas as pd

from pandas.api.extensions import register_series_accessor
from dtoolkit.geoaccessor.series.to_geoframe import to_geoframe


@register_series_accessor("h3")
class H3:
    def __init__(self, s: pd.Series, /):
        # TODO: raise error if s.dtype is not int64 or str
        self.s = s

    def to_points(self, drop: bool = False) -> gpd.GeoSeries | gpd.GeoDataFrame:
        # TODO: Use `cell_to_latlng` instead of `h3_to_geo`
        # While h3-py release 4, `latlon_to_h3` is not available.

        # requires h3 >= 4
        # from h3.api.numpy_int import cell_to_latlng
        # requires h3 < 4
        from h3.api.numpy_int import h3_to_geo

        if not drop and self.s.name is None:
            raise ValueError(
                "to keep the original data requires setting the 'name' of "
                f"{s.__class__.__name__!r}.",
            )

        yx = np.asarray(s.apply(h3_to_geo).tolist())
        geometry = gpd.GeoSeries.from_xy(yx[:, 1], yx[:, 0], crs=4326)

        return geometry if drop else to_geoframe(s, geometry=geometry)

    def to_polygons(self, drop: bool = False) -> gpd.GeoSeries | gpd.GeoDataFrame:
        # TODO: Use `cell_to_boundary` instead of `h3_to_geo_boundary`
        # While h3-py release 4, `latlon_to_h3` is not available.

        # requires h3 >= 4
        # from h3.api.numpy_int import cell_to_boundary
        # requires h3 < 4
        from h3.api.numpy_int import h3_to_geo_boundary

        # TODO: delete pygeos after shapely 2.x released
        from pygeos import polygons

        if not drop and s.name is None:
            raise ValueError(
                "to keep the original data requires setting the 'name' of "
                f"{s.__class__.__name__!r}.",
            )

        geometry = np.asarray(s.apply(h3_to_geo_boundary).tolist())
        geometry = polygons(np.flip(geometry, 2))  # flip: (lat, lon) -> (lon, lat)
        geometry = gpd.GeoSeries(geometry, crs=4326)

        return geometry if drop else to_geoframe(s, geometry=geometry)
