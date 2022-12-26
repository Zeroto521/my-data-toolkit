from functools import wraps

import geopandas as gpd
import numpy as np
import pandas as pd
from pandas.api.extensions import register_index_accessor
from pandas.core.base import NoNewAttributesMixin
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.index.is_h3 import apply_h3
from dtoolkit.geoaccessor.index.is_h3 import is_h3


def available_if(check):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not check(args[0].index if isinstance(args[0], H3) else args[0]):
                raise TypeError(
                    f"For Non-H3 dtype, the '.h3.{func.__name__}' is not available.",
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator


@register_index_accessor("h3")
@doc(klass="Index")
class H3(NoNewAttributesMixin):
    """
    Hexagonal hierarchical geospatial indexing system.

    A little magic binding H3 for :obj:`~pandas.{klass}`.

    Raises
    ------
    ModuleNotFoundError
        If don't have module named 'h3'.

    TypeError
        If not Index(string) or Index(int64) dtype.

    See Also
    --------
    dtoolkit.geoaccessor.index.H3
    dtoolkit.geoaccessor.series.H3
    dtoolkit.geoaccessor.dataframe.H3

    Notes
    -----
    Based on pandas style, APIs are designed as follows:

    - Remove the prefix ``h3_`` of the original H3 API.
      e.g. :meth:`h3.cell_to_latlng` → :meth:`~dtoolkit.geoaccessor.series.H3.to_points`

    - Use ``to_`` prefix for the conversion between H3 cell int and str.
      e.g. :meth:`h3.int_to_str` → :meth:`~dtoolkit.geoaccessor.series.H3.to_str`

    - Use ``is_`` prefix for the validation of H3 cell.
      e.g. :meth:`h3.is_valid_cell` → :meth:`~dtoolkit.geoaccessor.series.H3.is_valid`
    """

    def __init__(self, index: pd.Index, /):
        self.index = index

        self._freeze()

    @property
    @available_if(is_h3)
    def area(self) -> pd.Series:
        r"""
        Compute the spherical surface area of a specific H3 cell.

        Returns
        -------
        Series(float64)
            With H3 cell as the its index. Its values are the spherical surface area
            of the H3 cell and unit is m\ :sup:`2`.

        See Also
        --------
        h3.cell_area
        dtoolkit.geoaccessor.index.H3.area
        dtoolkit.geoaccessor.series.H3.area
        dtoolkit.geoaccessor.dataframe.H3.area

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> s = pd.Series(['a', 'b'], index=[612845052823076863, 614269156845420543])
        >>> s
        612845052823076863    a
        614269156845420543    b
        dtype: object
        >>> s.h3.area
        612845052823076863    710781.770906
        614269156845420543    852134.191671
        dtype: float64
        """

        return pd.Series(
            apply_h3(self.index, "cell_area", unit="m^2"),
            index=self.index,
        )

        # TODO: Available only for h3 release 4.
        # @property
        # @available_if(is_h3)
        # def edge(self) -> pd.Series:
        #     """
        #     Compute the spherical length of a specific H3 edge.

        #     Returns
        #     -------
        #     Series(float64)
        #         With H3 cell as the its index. Its values are the spherical length
        #         of the H3 edge and unit is m.

        #     See Also
        #     --------
        #     h3.edge_length
        #     dtoolkit.geoaccessor.index.H3.edge
        #     dtoolkit.geoaccessor.series.H3.edge
        #     dtoolkit.geoaccessor.dataframe.H3.edge
        #     """

        #     return pd.Series(
        #         apply_h3(self.index, "edge_length", unit="m"),
        #         index=self.index,
        #     )

    @property
    @available_if(is_h3)
    def resolution(self) -> pd.Series:
        """
        Return the resolution of H3 cell.

        Returns
        -------
        Series(int64)
            With H3 cell as the its index. Its values are the resolution of the H3 cell.

        See Also
        --------
        h3.get_resolution
        dtoolkit.geoaccessor.index.H3.resolution
        dtoolkit.geoaccessor.series.H3.resolution
        dtoolkit.geoaccessor.dataframe.H3.resolution
        dtoolkit.geoaccessor.index.H3.is_res_class_III
        dtoolkit.geoaccessor.series.H3.is_res_class_III
        dtoolkit.geoaccessor.dataframe.H3.is_res_class_III

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> s = pd.Series(['a', 'b'], index=[612845052823076863, 614269156845420543])
        >>> s
        612845052823076863    a
        614269156845420543    b
        dtype: object
        >>> s.h3.resolution
        612845052823076863    8
        614269156845420543    8
        dtype: int64
        """
        # TODO: Use `get_resolution` instead of `h3_get_resolution`
        # While h3-py release 4, `get_resolution` is not available.
        return pd.Series(
            apply_h3(self.index, "h3_get_resolution"),
            index=self.index,
        )

    @property
    def is_valid(self) -> pd.Series:
        """
        Validates H3 cell (hexagon or pentagon).

        Returns
        -------
        Series(bool)
            With H3 cell as the its index. Its values indicating whether the H3 cell is
            valid.

        See Also
        --------
        h3.is_valid_cell
        dtoolkit.geoaccessor.index.is_h3
        dtoolkit.geoaccessor.series.is_h3
        dtoolkit.geoaccessor.dataframe.is_h3
        dtoolkit.geoaccessor.index.H3.is_valid
        dtoolkit.geoaccessor.series.H3.is_valid
        dtoolkit.geoaccessor.dataframe.H3.is_valid

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd

        String type H3 cell index.

        >>> s = pd.Series(
        ...     ['a', 'b', 'c', 'd'],
        ...     index=[0, 'hello', 'world', '88143541bdfffff'],
        ... )
        >>> s
        0                  a
        hello              b
        world              c
        88143541bdfffff    d
        dtype: object
        >>> s.h3.is_valid
        0                  False
        hello              False
        world              False
        88143541bdfffff     True
        dtype: bool

        Int type H3 cell index.

        >>> s = pd.Series(
        ...     ['a', 'b', 'c', 'd'],
        ...     index=[
        ...         1,
        ...         10,
        ...         100000000000000000,
        ...         612845052823076863,
        ...     ],
        ... )
        >>> s
        1                     a
        10                    b
        100000000000000000    c
        612845052823076863    d
        dtype: object
        >>> s.h3.is_valid
        1                     False
        10                    False
        100000000000000000    False
        612845052823076863     True
        dtype: bool
        """
        # TODO: Use `is_valid_cell` instead of `h3_is_valid`
        # While h3-py release 4, `is_valid_cell` is not available.
        return pd.Series(
            apply_h3(self.index, "h3_is_valid"),
            index=self.index,
        )

    @property
    @available_if(is_h3)
    def is_pentagon(self) -> pd.Series:
        """
        Identify if H3 cell is a pentagon.

        Returns
        -------
        Series(bool)
            With H3 cell as the its index. Its values indicating whether the H3 cell is
            a pentagon.

        See Also
        --------
        h3.is_pentagon
        dtoolkit.geoaccessor.index.H3.is_pentagon
        dtoolkit.geoaccessor.series.H3.is_pentagon
        dtoolkit.geoaccessor.dataframe.H3.is_pentagon

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> s = pd.Series(['a', 'b'], index=[612845052823076863, 614269156845420543])
        >>> s
        612845052823076863    a
        614269156845420543    b
        dtype: object
        >>> s.h3.is_pentagon
        612845052823076863    False
        614269156845420543    False
        dtype: bool
        """
        # TODO: Use `is_pentagon` instead of `h3_is_pentagon`
        # While h3-py release 4, `is_pentagon` is not available.
        return pd.Series(
            apply_h3(self.index, "h3_is_pentagon"),
            index=self.index,
        )

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
        Series(bool)
            With H3 cell as the its index. Its values indicating whether the H3 cell
            is Class III resolution.

        See Also
        --------
        h3.is_res_class_III
        dtoolkit.geoaccessor.index.H3.resolution
        dtoolkit.geoaccessor.series.H3.resolution
        dtoolkit.geoaccessor.dataframe.H3.resolution
        dtoolkit.geoaccessor.index.H3.is_res_class_III
        dtoolkit.geoaccessor.series.H3.is_res_class_III
        dtoolkit.geoaccessor.dataframe.H3.is_res_class_III

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> s = pd.Series(['a', 'b'], index=[612845052823076863, 614269156845420543])
        >>> s
        612845052823076863    a
        614269156845420543    b
        dtype: object
        >>> s.h3.is_res_class_III
        612845052823076863    False
        614269156845420543    False
        dtype: bool
        """
        # TODO: Use `is_res_class_III` instead of `h3_is_res_class_III`
        # While h3-py release 4, `is_res_class_III` is not available.
        return pd.Series(
            apply_h3(self.index, "h3_is_res_class_III"),
            index=self.index,
        )

    @available_if(is_h3)
    def to_int(self) -> pd.Index:
        """
        Converts hexadecimal string H3 cell index to 64-bit integer.

        Returns
        -------
        Index(int64)

        Raises
        ------
        TypeError
            If the Index dtype is not string.

        See Also
        --------
        h3.str_to_int
        dtoolkit.geoaccessor.index.H3.to_str
        dtoolkit.geoaccessor.series.H3.to_int
        dtoolkit.geoaccessor.dataframe.H3.to_int

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> index = pd.Index(['88143541bdfffff', '886528b2a3fffff'])
        >>> index
        Index(['88143541bdfffff', '886528b2a3fffff'], dtype='object')
        >>> index.h3.to_int()
        Int64Index([612845052823076863, 614269156845420543], dtype='int64')
        """
        # TODO: Use `str_to_int` instead of `string_to_h3`
        # While h3-py release 4, `str_to_int` is not available.
        from pandas.api.types import is_string_dtype
        from h3.api.numpy_int import string_to_h3

        if not is_string_dtype(self.index):
            raise TypeError(f"Expected Index(string), but got {self.index.dtype!r}.")
        return self.index.map(string_to_h3)

    @available_if(is_h3)
    def to_str(self) -> pd.Index:
        """
        Converts 64-bit integer H3 cell index to hexadecimal string.

        Returns
        -------
        Index(string)

        Raises
        ------
        TypeError
            If the Index dtype is not int64.

        See Also
        --------
        h3.int_to_str
        dtoolkit.geoaccessor.index.H3.to_int
        dtoolkit.geoaccessor.series.H3.to_str
        dtoolkit.geoaccessor.dataframe.H3.to_str

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> index = pd.Index([612845052823076863, 614269156845420543])
        >>> index
        Int64Index([612845052823076863, 614269156845420543], dtype='int64')
        >>> index.h3.to_str()
        Index(['88143541bdfffff', '886528b2a3fffff'], dtype='object')
        """
        # TODO: Use `int_to_str` instead of `h3_to_string`
        # While h3-py release 4, `int_to_str` is not available.
        from pandas.api.types import is_integer_dtype
        from h3.api.numpy_int import h3_to_string

        if not is_integer_dtype(self.index):
            raise TypeError(f"Expected Index(int64), but got {self.index.dtype!r}.")
        return self.index.map(h3_to_string)

    @available_if(is_h3)
    def to_center_child(self, resolution: int = None) -> pd.Index:
        """
        Get the center child of cell.

        Parameters
        ----------
        resolution : int, optional
            The resolution for the children. If None, then use the current
            ``resolution`` of cell ``+1`` .

        Returns
        -------
        Index
            New H3 center child cell.

        See Also
        --------
        h3.cell_to_center_child
        dtoolkit.geoaccessor.index.H3.to_children
        dtoolkit.geoaccessor.series.H3.to_center_child
        dtoolkit.geoaccessor.dataframe.H3.to_center_child

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> index = pd.Index([612845052823076863, 614269156845420543])
        >>> index
        Int64Index([612845052823076863, 614269156845420543], dtype='int64')
        >>> index.h3.to_center_child()
        Int64Index([617348652448612351, 618772756470956031], dtype='int64')
        """
        # TODO: Use `cell_to_center_child` instead of `h3_to_center_child`
        # While h3-py release 4, `cell_to_center_child` is not available.
        return apply_h3(self.index, "h3_to_center_child", res=resolution)

    @available_if(is_h3)
    def to_children(self, resolution: int = None) -> pd.Index:
        """
        Get the children of cell.

        Parameters
        ----------
        resolution : int, optional
            The resolution for the children. If None, then use the current
            ``resolution`` of cell ``+1`` .

        Returns
        -------
        Index
            New H3 children cells.

        See Also
        --------
        h3.cell_to_children
        dtoolkit.geoaccessor.index.H3.to_center_child
        dtoolkit.geoaccessor.index.H3.to_parent
        dtoolkit.geoaccessor.series.H3.to_children
        dtoolkit.geoaccessor.dataframe.H3.to_children

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> index = pd.Index([612845052823076863, 614269156845420543])
        >>> index
        Int64Index([612845052823076863, 614269156845420543], dtype='int64')
        >>> index.h3.to_children()  # doctest: +SKIP
        Index(
            [
                [
                    617348652448612351,
                    617348652448874495,
                    617348652449136639,
                    617348652449398783,
                    617348652449660927,
                    617348652449923071,
                    617348652450185215
                ],
                [
                    618772756470956031,
                    618772756471218175,
                    618772756471480319,
                    618772756471742463,
                    618772756472004607,
                    618772756472266751,
                    618772756472528895
                ]
            ]
            dtype='object'
        )
        """
        # TODO: Use `cell_to_children` instead of `h3_to_children`
        # While h3-py release 4, `cell_to_children` is not available.
        return apply_h3(self.index, "h3_to_children", res=resolution)

    @available_if(is_h3)
    def to_parent(self, resolution: int = None) -> pd.Index:
        """
        Get the parent of cell.

        Parameters
        ----------
        resolution : int, optional
            The resolution for the children. If None, then use the current
            ``resolution`` of cell ``-1`` .

        Returns
        -------
        Index
            New H3 parent cell.

        See Also
        --------
        h3.cell_to_parent
        dtoolkit.geoaccessor.index.H3.to_children
        dtoolkit.geoaccessor.series.H3.to_parent
        dtoolkit.geoaccessor.dataframe.H3.to_parent

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> index = pd.Index([612845052823076863, 614269156845420543])
        >>> index
        Int64Index([612845052823076863, 614269156845420543], dtype='int64')
        >>> index.h3.to_parent()
        Int64Index([608341453197803519, 609765557230632959], dtype='int64')
        """
        # TODO: Use `cell_to_parent` instead of `h3_to_parent`
        # While h3-py release 4, `cell_to_parent` is not available.
        return apply_h3(self.index, "h3_to_parent", res=resolution)

    @available_if(is_h3)
    def to_points(self) -> gpd.GeoSeries:
        """
        Return the center :obj:`~shapely.Point` of H3 cell.

        Returns
        -------
        GeoSeries
            With H3 cell as the its index.

        See Also
        --------
        h3.cell_to_latlng
        dtoolkit.geoaccessor.index.H3.to_polygons
        dtoolkit.geoaccessor.series.H3.to_points
        dtoolkit.geoaccessor.dataframe.H3.to_polygons
        dtoolkit.geoaccessor.geoseries.to_h3

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> index = pd.Index([612845052823076863, 614269156845420543])
        >>> index
        Int64Index([612845052823076863, 614269156845420543], dtype='int64')
        >>> index.h3.to_points()
        612845052823076863  POINT (121.99637 55.00331)
        614269156845420543    POINT (99.99611 0.99919)
        dtype: geometry
        """
        # TODO: Use `cell_to_latlng` instead of `h3_to_geo`
        # While h3-py release 4, `cell_to_latlng` is not available.
        yx = np.asarray(apply_h3(self.index, "h3_to_geo").tolist())
        return gpd.GeoSeries.from_xy(yx[:, 1], yx[:, 0], crs=4326, index=self.index)

    @available_if(is_h3)
    def to_polygons(self) -> gpd.GeoSeries:
        """
        Return :obj:`~shapely.Polygon` to describe the cell boundary.

        Returns
        -------
        GeoSeries
            With H3 cell as the its index.

        See Also
        --------
        h3.cell_to_boundary
        dtoolkit.geoaccessor.index.H3.to_points
        dtoolkit.geoaccessor.series.H3.to_polygons
        dtoolkit.geoaccessor.dataframe.H3.to_points
        dtoolkit.geoaccessor.geoseries.to_h3

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> index = pd.Index([612845052823076863, 614269156845420543])
        >>> index
        Int64Index([612845052823076863, 614269156845420543], dtype='int64')
        >>> index.h3.to_polygons()
        612845052823076863  POLYGON ((121.98797 55.00408, 121.99122 54.999...
        614269156845420543  POLYGON ((100.00035 0.99630, 100.00080 1.00141...
        dtype: geometry
        """
        from shapely import polygons

        # TODO: Use `cell_to_boundary` instead of `h3_to_geo_boundary`
        # While h3-py release 4, `cell_to_boundary` is not available.
        return gpd.GeoSeries(
            polygons(
                apply_h3(
                    self.index,
                    "h3_to_geo_boundary",
                    geo_json=True,
                ).tolist(),
            ),
            crs=4326,
            index=self.index,
        )
