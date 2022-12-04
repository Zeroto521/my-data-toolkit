from __future__ import annotations

from functools import wraps
from typing import Literal

import geopandas as gpd
import numpy as np
import pandas as pd
from pandas.api.extensions import register_series_accessor

from dtoolkit.geoaccessor.series.to_geoframe import to_geoframe


def available_if(check):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not check(args[0]):
                raise TypeError(
                    f"For Non-H3, the '.h3.{func.__name__}' is not available."
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator


@register_series_accessor("h3")
class H3:
    """
    Hexagonal hierarchical geospatial indexing system.

    A little magic binding H3 for Series.

    Based on ``pandas.Series`` API style, this accessor APIs are designed as follows:

    - Remove the prefix `h3_` of the original H3 API.
      e.g. :meth:`h3.h3_to_geometh` → :meth:`~dtoolkit.geoaccessor.series.H3.to_points`

    - Use `to_` prefix for the conversion between H3 cell int and str.
      e.g. :meth:`h3.h3_to_stringmeth` → :meth:`~dtoolkit.geoaccessor.series.H3.to_str`

    - Use `is_` prefix for the validation of H3 cell.
      e.g. :meth:`h3.h3_is_validmeth` → :meth:`~dtoolkit.geoaccessor.series.H3.is_valid`

    Notes
    -----
    Default use :meth:`h3.api.numpy_intmeth` as the backend. So the IO will use int64.
    It can be converted to str by :meth:`~dtoolkit.geoaccessor.series.H3.to_str()`
    and converted to int by :meth:`~dtoolkit.geoaccessor.series.H3.to_int()``.
    """

    def __init__(self, s: pd.Series, /):
        self.s = s

    @property
    def is_valid(self) -> pd.Series:
        """
        Validates an H3 cell (hexagon or pentagon).

        Returns
        -------
        Series
            Boolean Series indicating whether the H3 cell is valid.

        See Also
        --------
        h3.h3_is_valid
        """
        # TODO: Use `is_valid_cell` instead of `h3_is_valid`
        # While h3-py release 4, `is_valid_cell` is not available.

        # requires h3 >= 4
        # from h3.api.numpy_int import is_valid_cell
        # requires h3 < 4
        from h3.api.numpy_int import h3_is_valid

        return self.s.apply(h3_is_valid)

    def is_h3(self) -> bool:
        """
        Validate whether the whole series is H3 cell index.

        Returns
        -------
        bool
            True if the whole series is H3 cell index else False.

        See Also
        --------
        h3.h3_is_valid
        """

        return all(self.is_valid)

    @property
    @available_if(is_h3)
    def is_res_class_III(self) -> pd.Series:
        """
        Determine if cell has orientation "Class II" or "Class III".

        Cells of resolutions:

        - Class II: 0, 2, 4, 6, 8, 10, 12, 14
        - Class III: 1, 3, 5, 7, 9, 11, 13, 15

        Returns
        -------
        Series
            Boolean Series indicating whether the H3 cell is Class III.

        See Also
        --------
        h3.h3_is_res_class_III
        """
        # TODO: Use `is_res_class_III` instead of `h3_is_res_class_III`
        # While h3-py release 4, `is_res_class_III` is not available.

        # requires h3 >= 4
        # from h3.api.numpy_int import is_res_class_III
        # requires h3 < 4
        from h3.api.numpy_int import h3_is_res_class_III

        return self.s.apply(h3_is_res_class_III)

    @property
    @available_if(is_h3)
    def is_pentagon(self) -> pd.Series:
        """
        Identify if an H3 cell is a pentagon.

        Returns
        -------
        Series
            Boolean Series indicating whether the H3 cell is a pentagon.

        See Also
        --------
        h3.h3_is_pentagon
        """
        # TODO: Use `is_pentagon` instead of `h3_is_pentagon`
        # While h3-py release 4, `is_pentagon` is not available.

        # requires h3 >= 4
        # from h3.api.numpy_int import is_pentagon
        # requires h3 < 4
        from h3.api.numpy_int import h3_is_pentagon

        return self.s.apply(h3_is_pentagon)

    @property
    @available_if(is_h3)
    def resolution(self) -> pd.Series:
        """
        Return the resolution of an H3 cell.

        Returns
        -------
        Series
            Integer Series indicating the resolution of the H3 cell.

        See Also
        --------
        h3.h3_get_resolution
        """
        # TODO: Use `get_resolution` instead of `h3_get_resolution`
        # While h3-py release 4, `get_resolution` is not available.

        # requires h3 >= 4
        # from h3.api.numpy_int import get_resolution
        # requires h3 < 4
        from h3.api.numpy_int import h3_get_resolution

        return self.s.apply(h3_get_resolution)

    @property
    @available_if(is_h3)
    def edge_length(self) -> pd.Series:
        """
        Compute the spherical length of a specific H3 edge.

        Returns
        -------
        Series
            Float (unit is m) Series indicating the spherical length of the H3 edge.

        See Also
        --------
        h3.edge_length
        """
        from h3.api.numpy_int import edge_length

        return self.s.apply(edge_length, unit="m")

    @property
    @available_if(is_h3)
    def area(self) -> pd.Series:
        """
        Compute the spherical surface area of a specific H3 cell.

        Returns
        -------
        Series
            Float (unit is m\ :sup:`2`) Series indicating the spherical surface area
            of the H3 cell.

        See Also
        --------
        h3.cell_area
        """
        from h3.api.numpy_int import cell_area

        return self.s.apply(cell_area, unit="m^2")

    def to_str(self) -> pd.Series:
        """
        Converts a hexadecimal string to an H3 64-bit integer index.

        Returns
        -------
        Series
            String Series indicating the H3 cell index.

        Raises
        ------
        TypeError
            If the Series is not int type H3 cell index.

        See Also
        --------
        h3.h3_to_string
        """
        # TODO: Use `int_to_str` instead of `h3_to_string`
        # While h3-py release 4, `int_to_str` is not available.

        # requires h3 >= 4
        # from h3.api.numpy_int import int_to_str
        # requires h3 < 4
        from h3.api.numpy_int import h3_to_string

        from pandas.api.types import is_integer_dtype

        if not is_integer_dtype(self.s):
            raise TypeError(
                f"The dtype of the series must be 'int', but got {self.s.dtype!r}.",
            )
        return self.s.apply(h3_to_string)

    def to_int(self) -> pd.Series:
        """
        Converts an H3 64-bit integer index to a hexadecimal string.

        Returns
        -------
        Series
            Integer Series indicating the H3 cell index.

        Raises
        ------
        TypeError
            If the Series is not str type H3 cell index.

        See Also
        --------
        h3.h3_to_int
        """
        # TODO: Use `str_to_int` instead of `string_to_h3`
        # While h3-py release 4, `str_to_int` is not available.

        # requires h3 >= 4
        # from h3.api.numpy_int import str_to_int
        # requires h3 < 4
        from h3.api.numpy_int import string_to_h3

        from pandas.api.types import is_string_dtype

        if not is_string_dtype(self.s):
            raise TypeError(
                f"The dtype of the series must be 'str', but got {self.s.dtype!r}.",
            )
        return self.s.apply(string_to_h3)

    @available_if(is_h3)
    def to_points(self, drop: bool = False) -> gpd.GeoSeries | gpd.GeoDataFrame:
        """
        Return the center Point of an H3 cell as a lat/lng pair.

        Parameters
        ----------
        drop : bool, default False
            Whether to drop the original H3 cell index column.

        Returns
        -------
        GeoSeries or GeoDataFrame
            If True, return a GeoSeries with the original H3 cell index column dropped.

        Raises
        ------
        ValueError
            If ``drop=False`` and the original H3 cell index column is not named.

        See Also
        --------
        h3.h3_to_geo
        """
        # TODO: Use `cell_to_latlng` instead of `h3_to_geo`
        # While h3-py release 4, `cell_to_latlng` is not available.

        # requires h3 >= 4
        # from h3.api.numpy_int import cell_to_latlng
        # requires h3 < 4
        from h3.api.numpy_int import h3_to_geo

        if not drop and self.s.name is None:
            raise ValueError(
                "to keep the original data requires setting the 'name' of "
                f"{self.s.__class__.__name__!r}.",
            )

        yx = np.asarray(self.s.apply(h3_to_geo).tolist())
        geometry = gpd.GeoSeries.from_xy(yx[:, 1], yx[:, 0], crs=4326)

        return geometry if drop else to_geoframe(self.s, geometry=geometry)

    @available_if(is_h3)
    def to_polygons(self, drop: bool = False) -> gpd.GeoSeries | gpd.GeoDataFrame:
        # TODO: Use `cell_to_boundary` instead of `h3_to_geo_boundary`
        # While h3-py release 4, `cell_to_boundary` is not available.

        # requires h3 >= 4
        # from h3.api.numpy_int import cell_to_boundary
        # requires h3 < 4
        from h3.api.numpy_int import h3_to_geo_boundary

        # TODO: delete pygeos after shapely 2.x released
        from pygeos import polygons, to_shapely

        if not drop and self.s.name is None:
            raise ValueError(
                "to keep the original data requires setting the 'name' of "
                f"{self.s.__class__.__name__!r}.",
            )

        geometry = self.s.apply(h3_to_geo_boundary, geo_json=True).tolist()
        geometry = gpd.GeoSeries(to_shapely(polygons(geometry)), crs=4326)

        return geometry if drop else to_geoframe(self.s, geometry=geometry)

    @available_if(is_h3)
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

    @available_if(is_h3)
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

    @available_if(is_h3)
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
