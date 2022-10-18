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
        # TODO: Use `is_valid_cell` instead of `h3_is_valid`
        # While h3-py release 4, `is_valid_cell` is not available.

        # requires h3 >= 4
        # from h3.api.numpy_int import is_valid_cell
        # requires h3 < 4
        from h3.api.numpy_int import h3_is_valid

        return self.s.apply(h3_is_valid)

    @property
    def is_res_class_III(self) -> pd.Series:
        from h3.api.numpy_int import is_res_class_III

        return self.s.apply(is_res_class_III)

    @property
    def is_pentagon(self) -> pd.Series:
        from h3.api.numpy_int import is_pentagon

        return self.s.apply(is_pentagon)

    @property
    def edge_length(self) -> pd.Series:
        from h3.api.numpy_int import edge_length

        return self.s.apply(edge_length, unit="m")

    @property
    def area(self) -> pd.Series:
        from h3.api.numpy_int import cell_area

        return self.s.apply(cell_area, unit="m^2")

    def to_str(self) -> pd.Series:
        # TODO: Use `int_to_str` instead of `h3_to_string`
        # While h3-py release 4, `int_to_str` is not available.

        # requires h3 >= 4
        # from h3.api.numpy_int import int_to_str
        # requires h3 < 4
        from h3 import h3_to_string


        return self.s if self.s.dtype == "str" else self.s.apply(h3_to_string)

    def to_int(self) -> pd.Series:
        # TODO: Use `str_to_int` instead of `string_to_h3`
        # While h3-py release 4, `str_to_int` is not available.

        # requires h3 >= 4
        # from h3.api.numpy_int import str_to_int
        # requires h3 < 4
        from h3 import string_to_h3

        return self.s if self.s.dtype == "int64" else self.s.apply(string_to_h3)

    def to_points(self, drop: bool = False) -> gpd.GeoSeries | gpd.GeoDataFrame:
        # TODO: Use `cell_to_latlng` instead of `h3_to_geo`
        # While h3-py release 4, `cell_to_latlng` is not available.

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
        # While h3-py release 4, `cell_to_boundary` is not available.

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

    def to_children(
        self,
        resolution: int = None,
        *,
        drop: bool = True,
        partent: Hashable = "partent",
        children: Hashable = "children",
    ) -> pd.Series | pd.DataFrame:
        # TODO: Use `cell_to_children` instead of `h3_to_children`
        # While h3-py release 4, `cell_to_children` is not available.

        # requires h3 >= 4
        # from h3.api.numpy_int import cell_to_children
        # requires h3 < 4
        from h3.api.numpy_int import h3_to_children

        from dtoolkit.accessor.series import len as s_len

        h3_list = self.s.apply(h3_to_children, res=resolution)
        h3_children = h3_list.explode(ignore_index=True)

        if drop:
            return h3_children
        return pd.concat(
            (
                (
                    self.s.repeat(s_len(h3_list))
                    .reset_index(drop=True)
                    .rename(self.s.name or partent)
                ),
                h3_children.rename(children),
            ),
            axis=1,
        )

    def to_parent(
        self,
        resolution: int = None,
        *,
        drop: bool = True,
        partent: Hashable = "partent",
        children: Hashable = "children",
    ) -> pd.Series | pd.DataFrame:
        # TODO: Use `cell_to_parent` instead of `h3_to_children`
        # While h3-py release 4, `cell_to_parent` is not available.

        # requires h3 >= 4
        # from h3.api.numpy_int import cell_to_parent
        # requires h3 < 4
        from h3.api.numpy_int import h3_to_parent

        h3_parent = self.s.apply(h3_to_parent, res=resolution)

        if drop:
            return h3_parent
        return pd.concat(
            (
                h3_parent.rename(partent),
                self.s.rename(self.s.name or children),
            ),
            axis=1,
        )

    def to_center_child(
        self,
        resolution: int = None,
        *,
        drop: bool = True,
        partent: Hashable = "partent",
        children: Hashable = "children",
    ) -> pd.Series | pd.DataFrame:
        # TODO: Use `cell_to_center_child` instead of `h3_to_center_child`
        # While h3-py release 4, `cell_to_center_child` is not available.

        # requires h3 >= 4
        # from h3.api.numpy_int import cell_to_center_child
        # requires h3 < 4
        from h3.api.numpy_int import h3_to_center_child

        h3_children = self.s.apply(h3_to_center_child, res=resolution)

        if drop:
            return h3_children
        return pd.concat(
            (
                self.s.rename(self.s.name or partent),
                h3_children.rename(children),
            ),
            axis=1,
        )
