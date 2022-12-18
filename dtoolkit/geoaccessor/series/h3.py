from __future__ import annotations

from dataclasses import dataclass
from functools import wraps
from typing import Hashable

import geopandas as gpd
import numpy as np
import pandas as pd
from pandas.api.extensions import register_series_accessor
from pandas.api.types import is_int64_dtype
from pandas.api.types import is_string_dtype
from shapely import polygons

from dtoolkit.accessor.series import len as s_len
from dtoolkit.geoaccessor.series.is_h3 import is_h3
from dtoolkit.geoaccessor.series.is_h3 import method_from_h3
from dtoolkit.geoaccessor.series.to_geoframe import to_geoframe


def available_if(check):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not check(args[0].s if isinstance(args[0], H3) else args[0]):
                raise TypeError(
                    f"For Non-H3 dtype, the '.h3.{func.__name__}' is not available.",
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator


@register_series_accessor("h3")
@dataclass
class H3:
    """
    Hexagonal hierarchical geospatial indexing system.

    A little magic binding H3 for Series.

    Raises
    ------
    ModuleNotFoundError
        If don't have module named 'h3'.

    TypeError
        If not Series(string) or Series(int64) dtype.

    Notes
    -----
    Based on :obj:`pandas.Series` API style, this accessor APIs are designed as follows:

    - Remove the prefix `h3_` of the original H3 API.
      e.g. :meth:`h3.h3_to_geo` → :meth:`~dtoolkit.geoaccessor.series.H3.to_points`

    - Use `to_` prefix for the conversion between H3 cell int and str.
      e.g. :meth:`h3.h3_to_string` → :meth:`~dtoolkit.geoaccessor.series.H3.to_str`

    - Use `is_` prefix for the validation of H3 cell.
      e.g. :meth:`h3.h3_is_valid` → :meth:`~dtoolkit.geoaccessor.series.H3.is_valid`
    """

    s: pd.Series

    @property
    @available_if(is_h3)
    def area(self) -> pd.Series:
        r"""
        Compute the spherical surface area of a specific H3 cell.

        Returns
        -------
        Series
            Float (unit is m\ :sup:`2`) Series indicating the spherical surface area
            of the H3 cell.

        See Also
        --------
        h3.cell_area

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> s = pd.Series([612845052823076863, 614269156845420543])
        >>> s
        0    612845052823076863
        1    614269156845420543
        dtype: int64
        >>> s.h3.area
        0    710781.770905
        1    852134.191672
        dtype: float64
        """

        return self.s.apply(method_from_h3(self.s, "cell_area"), unit="m^2")

    @property
    @available_if(is_h3)
    def edge(self) -> pd.Series:
        """
        Compute the spherical length of a specific H3 edge.

        .. warning::
            Available only for h3 release 4.

        Returns
        -------
        Series
            Float (unit is m) Series indicating the spherical length of the H3 edge.

        See Also
        --------
        h3.edge_length

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> s = pd.Series([612845052823076863, 614269156845420543])
        >>> s
        0    612845052823076863
        1    614269156845420543
        dtype: int64
        >>> s.h3.edge
        0    8
        1    8
        dtype: int64
        """

        return self.s.apply(method_from_h3(self.s, "edge_length"), unit="m")

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
        h3.get_resolution

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> s = pd.Series([612845052823076863, 614269156845420543])
        >>> s
        0    612845052823076863
        1    614269156845420543
        dtype: int64
        >>> s.h3.resolution
        0    8
        1    8
        dtype: int64
        """

        # TODO: Use `get_resolution` instead of `h3_get_resolution`
        # While h3-py release 4, `get_resolution` is not available.
        return self.s.apply(method_from_h3(self.s, "h3_get_resolution"))

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
        h3.is_valid_cell
        dtoolkit.geoaccessor.series.is_h3

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd

        Str type H3 cell index.

        >>> s = pd.Series([0, 'hello', 'world', '88143541bdfffff'])
        >>> s
        0                  0
        1              hello
        2              world
        3    88143541bdfffff
        dtype: object
        >>> s.h3.is_valid
        0    False
        1    False
        2    False
        3     True
        dtype: bool

        Int type H3 cell index.

        >>> s = pd.Series([
        ...     1,
        ...     10,
        ...     100000000000000000,
        ...     612845052823076863,
        ... ])
        >>> s
        0                     1
        1                    10
        2    100000000000000000
        3    612845052823076863
        dtype: int64
        >>> s.h3.is_valid
        0    False
        1    False
        2    False
        3     True
        dtype: bool
        """

        # TODO: Use `is_valid_cell` instead of `h3_is_valid`
        # While h3-py release 4, `is_valid_cell` is not available.
        return self.s.apply(method_from_h3(self.s, "h3_is_valid"))

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
        h3.is_pentagon

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> s = pd.Series([612845052823076863, 614269156845420543])
        >>> s
        0    612845052823076863
        1    614269156845420543
        dtype: int64
        >>> s.h3.is_pentagon
        0    False
        1    False
        dtype: bool
        """

        # TODO: Use `is_pentagon` instead of `h3_is_pentagon`
        # While h3-py release 4, `is_pentagon` is not available.
        return self.s.apply(method_from_h3(self.s, "h3_is_pentagon"))

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
        h3.is_res_class_III

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> s = pd.Series([612845052823076863, 614269156845420543])
        >>> s
        0    612845052823076863
        1    614269156845420543
        dtype: int64
        >>> s.h3.is_res_class_III
        0    False
        1    False
        dtype: bool
        """

        # TODO: Use `is_res_class_III` instead of `h3_is_res_class_III`
        # While h3-py release 4, `is_res_class_III` is not available.
        return self.s.apply(method_from_h3(self.s, "h3_is_res_class_III"))

    @available_if(is_h3)
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
            If the dtype of the Series is not string.

        See Also
        --------
        h3.str_to_int

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> s = pd.Series(['88143541bdfffff', '886528b2a3fffff'])
        >>> s
        0    88143541bdfffff
        1    886528b2a3fffff
        dtype: object
        >>> s.h3.to_str()
        0    612845052823076863
        1    614269156845420543
        dtype: int64
        """
        # TODO: Use `str_to_int` instead of `string_to_h3`
        # While h3-py release 4, `str_to_int` is not available.
        from h3.api.numpy_int import string_to_h3

        if not is_string_dtype(self.s):
            raise TypeError(f"Expected Series(string), but got {self.s.dtype!r}.")
        return self.s.apply(string_to_h3)

    @available_if(is_h3)
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
            If the dtype of the Series is not int64.

        See Also
        --------
        h3.int_to_str

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> s = pd.Series([612845052823076863, 614269156845420543])
        >>> s
        0    612845052823076863
        1    614269156845420543
        dtype: int64
        >>> s.h3.to_str()
        0    88143541bdfffff
        1    886528b2a3fffff
        dtype: object
        """
        # TODO: Use `int_to_str` instead of `h3_to_string`
        # While h3-py release 4, `int_to_str` is not available.
        from h3.api.numpy_int import h3_to_string

        if not is_int64_dtype(self.s):
            raise TypeError(f"Expected Series(int64), but got {self.s.dtype!r}.")
        return self.s.apply(h3_to_string)

    @available_if(is_h3)
    def to_center_child(
        self,
        resolution: int = None,
        *,
        drop: bool = True,
        partent: Hashable = "partent",
        children: Hashable = "children",
    ) -> pd.Series | pd.DataFrame:
        """
        Get the center child of a cell at some finer resolution.

        Parameters
        ----------
        resolution : int, optional
            The resolution for the children. If None, then use the current
            ``resolution`` of cell ``+1`` .

        drop : bool, default True
            Whether to drop the original H3 cell index column.

        partent : Hashable, default "partent"
            The name of the partent cell column. If ``None`` then use ``s.name``.

        children : Hashable, default "children"
            The name of the children cell column.

        Returns
        -------
        Series or DataFrame
            If ``drop=True``, return a Series with the children cell index colum, else
            return a DataFrame with both the partent and children cell index columns.

        See Also
        --------
        h3.cell_to_center_child

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> s = pd.Series([612845052823076863, 614269156845420543], name='h3')
        >>> s
        0    612845052823076863
        1    614269156845420543
        Name: h3, dtype: int64
        >>> s.h3.to_center_child(drop=False, partent=None)
                           h3            children
        0  612845052823076863  617348652448612351
        1  614269156845420543  618772756470956031
        """
        # TODO: Use `cell_to_center_child` instead of `h3_to_center_child`
        # While h3-py release 4, `cell_to_center_child` is not available.
        h3_children = self.s.apply(
            method_from_h3(self.s, "h3_to_center_child"),
            res=resolution,
        )

        return (
            h3_children
            if drop
            else pd.concat(
                (
                    self.s.rename(partent or self.s.name),
                    h3_children.rename(children),
                ),
                axis=1,
            )
        )

    @available_if(is_h3)
    def to_children(
        self,
        resolution: int = None,
        *,
        drop: bool = True,
        partent: Hashable = "partent",
        children: Hashable = "children",
    ) -> pd.Series | pd.DataFrame:
        """
        Get the children of a cell.

        Parameters
        ----------
        resolution : int, optional
            The resolution for the children. If None, then use the current
            ``resolution`` of cell ``+1`` .

        drop : bool, default True
            Whether to drop the original H3 cell index column.

        partent : Hashable, default "partent"
            The name of the partent cell column. If ``None`` then use ``s.name``.

        children : Hashable, default "children"
            The name of the children cell column.

        Returns
        -------
        Series or DataFrame
            If ``drop=True``, return a Series with the children cell index colum, else
            return a DataFrame with both the partent and children cell index columns.

        See Also
        --------
        h3.cell_to_children

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> s = pd.Series([612845052823076863, 614269156845420543], name='h3')
        >>> s
        0    612845052823076863
        1    614269156845420543
        Name: h3, dtype: int64
        >>> s.h3.to_children(drop=False, partent=None)
                            h3            children
        0   612845052823076863  617348652448612351
        1   612845052823076863  617348652448874495
        2   612845052823076863  617348652449136639
        3   612845052823076863  617348652449398783
        4   612845052823076863  617348652449660927
        5   612845052823076863  617348652449923071
        6   612845052823076863  617348652450185215
        7   614269156845420543  618772756470956031
        8   614269156845420543  618772756471218175
        9   614269156845420543  618772756471480319
        10  614269156845420543  618772756471742463
        11  614269156845420543  618772756472004607
        12  614269156845420543  618772756472266751
        13  614269156845420543  618772756472528895
        """
        # TODO: Use `cell_to_children` instead of `h3_to_children`
        # While h3-py release 4, `cell_to_children` is not available.
        h3_list = self.s.apply(method_from_h3(self.s, "h3_to_children"), res=resolution)
        h3_children = h3_list.explode(ignore_index=True)

        return (
            h3_children
            if drop
            else pd.concat(
                (
                    (
                        self.s.repeat(s_len(h3_list))
                        .reset_index(drop=True)
                        .rename(partent or self.s.name)
                    ),
                    h3_children.rename(children),
                ),
                axis=1,
            )
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
        """
        Get the parent of a cell.

        Parameters
        ----------
        resolution : int, optional
            The resolution for the children. If None, then use the current
            ``resolution`` of cell ``-1`` .

        drop : bool, default True
            Whether to drop the original H3 cell index column.

        partent : Hashable, default "partent"
            The name of the partent cell column.

        children : Hashable, default "children"
            The name of the children cell column. If ``None`` then use ``s.name``.

        Returns
        -------
        Series or DataFrame
            If ``drop=True``, return a Series with the parent cell index colum, else
            return a DataFrame with both the partent and children cell index columns.

        See Also
        --------
        h3.cell_to_parent

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> s = pd.Series([612845052823076863, 614269156845420543], name='h3')
        >>> s
        0    612845052823076863
        1    614269156845420543
        Name: h3, dtype: int64
        >>> s.h3.to_parent(drop=False, children=None)
                      partent                  h3
        0  608341453197803519  612845052823076863
        1  609765557230632959  614269156845420543
        """
        # TODO: Use `cell_to_parent` instead of `h3_to_parent`
        # While h3-py release 4, `cell_to_parent` is not available.
        h3_parent = self.s.apply(method_from_h3(self.s, "h3_to_parent"), res=resolution)

        return (
            h3_parent
            if drop
            else pd.concat(
                (
                    h3_parent.rename(partent),
                    self.s.rename(children or self.s.name),
                ),
                axis=1,
            )
        )

    @available_if(is_h3)
    def to_points(self, drop: bool = False) -> gpd.GeoSeries | gpd.GeoDataFrame:
        """
        Return the center :obj:`~shapely.Point` of an H3 cell.

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
        h3.cell_to_latlng

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> s = pd.Series([612845052823076863, 614269156845420543], name='h3')
        >>> s
        0    612845052823076863
        1    614269156845420543
        Name: h3, dtype: int64
        >>> s.h3.to_points()
                           h3                    geometry
        0  612845052823076863  POINT (121.99637 55.00331)
        1  614269156845420543    POINT (99.99611 0.99919)
        """

        if not drop and self.s.name is None:
            raise ValueError(
                "to keep the original data requires setting the 'name' of "
                f"{self.s.__class__.__name__!r}.",
            )

        # TODO: Use `cell_to_latlng` instead of `h3_to_geo`
        # While h3-py release 4, `cell_to_latlng` is not available.
        yx = np.asarray(self.s.apply(method_from_h3(self.s, "h3_to_geo")).tolist())
        geometry = gpd.GeoSeries.from_xy(yx[:, 1], yx[:, 0], crs=4326)

        return geometry if drop else to_geoframe(self.s, geometry=geometry)

    @available_if(is_h3)
    def to_polygons(self, drop: bool = False) -> gpd.GeoSeries | gpd.GeoDataFrame:
        """
        Return :obj:`~shapely.Polygon` to describe the cell boundary.

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
        h3.cell_to_boundary

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> s = pd.Series([612845052823076863, 614269156845420543], name='h3')
        >>> s
        0    612845052823076863
        1    614269156845420543
        Name: h3, dtype: int64
        >>> s.h3.to_polygons()
                           h3                                           geometry
        0  612845052823076863  POLYGON ((121.98797 55.00408, 121.99122 54.999...
        1  614269156845420543  POLYGON ((100.00035 0.99630, 100.00080 1.00141...
        """

        if not drop and self.s.name is None:
            raise ValueError(
                "to keep the original data requires setting the 'name' of "
                f"{self.s.__class__.__name__!r}.",
            )

        # TODO: Use `cell_to_boundary` instead of `h3_to_geo_boundary`
        # While h3-py release 4, `cell_to_boundary` is not available.
        geometry = gpd.GeoSeries(
            polygons(
                self.s.apply(
                    method_from_h3(self.s, "h3_to_geo_boundary"),
                    geo_json=True,
                ).tolist(),
            ),
            crs=4326,
        )

        return geometry if drop else to_geoframe(self.s, geometry=geometry)
