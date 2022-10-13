from __future__ import annotations

from typing import Literal

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

    @classmethod
    def versions(cls) -> dict:
        from h3 import versions

        return versions()

    @classmethod
    def num_cells(cls, resolution: int) -> int:
        from h3 import get_num_cells

        return get_num_cells(resolution)

    @classmethod
    def res0_cells(cls) -> pd.Series:
        from h3.api.numpy_int import get_res0_cells

        return pd.Series(get_res0_cells())

    @classmethod
    def pentagons(cls, resolution: int) -> pd.Series:
        from h3.api.numpy_int import get_pentagons

        return pd.Series(get_pentagons(resolution))

    @property
    def resolution(self) -> pd.Series:
        from h3.api.numpy_int import get_resolution

        return self.s.apply(get_resolution)

    @property
    def is_valid(self) -> bool:
        from h3.api.numpy_int import is_valid_cell

        return self.s.apply(is_valid_cell)

    @property
    def is_res_class_III(self) -> pd.Series:
        from h3.api.numpy_int import is_res_class_III

        return self.s.apply(is_res_class_III)

    @property
    def is_pentagon(self) -> pd.Series:
        from h3.api.numpy_int import is_pentagon

        return self.s.apply(is_pentagon)

    def edge(self, unit: Literal["km", "m", "rads"] = "km") -> pd.Series:
        from h3.api.numpy_int import edge_length

        return self.s.apply(edge_length, unit=unit)

    def area(self, unit: Literal["km^2", "m^2", "rads^2"] = "km^2") -> pd.Series:
        from h3.api.numpy_int import cell_area

        return self.s.apply(cell_area, unit=unit)

    def to_str(self) -> pd.Series:
        from h3 import int_to_str

        return self.s if self.s.dtype == "str" else self.s.apply(int_to_str)

    def to_int(self) -> pd.Series:
        from h3 import str_to_int

        return self.s if self.s.dtype == "int64" else self.s.apply(str_to_int)

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
