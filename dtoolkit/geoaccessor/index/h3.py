from __future__ import annotations

from dataclasses import dataclass
from functools import wraps
from typing import Hashable
from functools import partial

import geopandas as gpd
import numpy as np
import pandas as pd
from pandas.api.extensions import register_index_accessor
from pandas.api.types import is_int64_dtype
from pandas.api.types import is_string_dtype
from shapely import polygons

from dtoolkit.accessor.series import len as s_len
from dtoolkit.geoaccessor.index.is_h3 import is_h3
from dtoolkit.geoaccessor.index.is_h3 import method_from_h3
from dtoolkit.geoaccessor.series.to_geoframe import to_geoframe


def available_if(check):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not check(args[0].index if isinstance(args[0], h3) else args[0]):
                raise TypeError(
                    f"For Non-H3 dtype, the '.h3.{func.__name__}' is not available.",
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator


@register_index_accessor("h3")
@dataclass
class h3:
    """
    Hexagonal hierarchical geospatial indexing system.

    A little magic binding H3 for Index.

    Raises
    ------
    ModuleNotFoundError
        If don't have module named 'h3'.

    TypeError
        If not Index(string) or Index(int64) dtype.

    Notes
    -----
    Based on :obj:`~pandas.Index` style, APIs are designed as follows:

    - Remove the prefix `h3_` of the original H3 API.
      e.g. :meth:`h3.h3_to_geo` → :meth:`~dtoolkit.geoaccessor.index.h3.to_points`

    - Use `to_` prefix for the conversion between H3 cell int and str.
      e.g. :meth:`h3.h3_to_string` → :meth:`~dtoolkit.geoaccessor.index.h3.to_str`

    - Use `is_` prefix for the validation of H3 cell.
      e.g. :meth:`h3.h3_is_valid` → :meth:`~dtoolkit.geoaccessor.index.h3.is_valid`
    """

    index: pd.Index

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

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> index = pd.Index([612845052823076863, 614269156845420543])
        Int64Index([612845052823076863, 614269156845420543], dtype='int64')
        >>> index.h3.area
        612845052823076863    710781.770906
        614269156845420543    852134.191671
        dtype: float64
        """

        func = partial(method_from_h3(self.index, "cell_area"), unit="m^2")
        return pd.Series(self.index.map(func), index=self.index)

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
    #     """

    #     func = partial(method_from_h3(self.index, "edge_length"), unit="m")
    #     return pd.Series(self.index.map(func), index=self.index)

    @property
    @available_if(is_h3)
    def resolution(self) -> pd.Series:
        """
        Return the resolution of an H3 cell.

        Returns
        -------
        Series(int64)
            With H3 cell as the its index. Its values are the resolution of the H3 cell.

        See Also
        --------
        h3.get_resolution
        dtoolkit.geoaccessor.index.h3.is_res_class_III

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> index = pd.Index([612845052823076863, 614269156845420543])
        Int64Index([612845052823076863, 614269156845420543], dtype='int64')
        >>> index.h3.resolution
        612845052823076863    8
        614269156845420543    8
        dtype: int64
        """

        # TODO: Use `get_resolution` instead of `h3_get_resolution`
        # While h3-py release 4, `get_resolution` is not available.
        return pd.Series(
            self.index.map(method_from_h3(self.index, "h3_get_resolution")),
            index=self.index,
        )

    @property
    def is_valid(self) -> pd.Series:
        """
        Validates an H3 cell (hexagon or pentagon).

        Returns
        -------
        Series(bool)
            Its values indicating whether the H3 cell is valid.

        See Also
        --------
        h3.is_valid_cell
        dtoolkit.geoaccessor.index.is_h3

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd

        String type H3 cell index.

        >>> index = pd.Index([0, 'hello', 'world', '88143541bdfffff'])
        >>> index
        Index([0, 'hello', 'world', '88143541bdfffff'], dtype='object')
        >>> index.h3.is_valid
        0                  False
        hello              False
        world              False
        88143541bdfffff     True
        dtype: bool
        Int type H3 cell index.

        >>> index = pd.Index([
        ...     1,
        ...     10,
        ...     100000000000000000,
        ...     612845052823076863,
        ... ])
        >>> index
        Int64Index([1, 10, 100000000000000000, 612845052823076863], dtype='int64')
        >>> index.h3.is_valid
        1                     False
        10                    False
        100000000000000000    False
        612845052823076863     True
        dtype: bool
        """

        # TODO: Use `is_valid_cell` instead of `h3_is_valid`
        # While h3-py release 4, `is_valid_cell` is not available.
        return pd.Series(
            self.index.map(method_from_h3(self.index, "h3_is_valid")),
            index=self.index,
        )


    @property
    @available_if(is_h3)
    def is_pentagon(self) -> pd.Series:
        """
        Identify if an H3 cell is a pentagon.

        Returns
        -------
        Series(bool)
            With H3 cell as the its index. Its values indicating whether the H3 cell is
            a pentagon.

        See Also
        --------
        h3.is_pentagon

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> index = pd.Index([612845052823076863, 614269156845420543])
        >>> index
        Int64Index([612845052823076863, 614269156845420543], dtype='int64')
        >>> index.h3.is_pentagon
        612845052823076863    False
        614269156845420543    False
        dtype: bool
        """

        # TODO: Use `is_pentagon` instead of `h3_is_pentagon`
        # While h3-py release 4, `is_pentagon` is not available.
        return pd.Series(
            self.index.map(method_from_h3(self.index, "h3_is_pentagon")),
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
        dtoolkit.geoaccessor.index.h3.resolution

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> index = pd.Series([612845052823076863, 614269156845420543])
        >>> index
        Int64Index([612845052823076863, 614269156845420543], dtype='int64')
        >>> index.h3.is_res_class_III
        612845052823076863    False
        614269156845420543    False
        dtype: bool
        """

        # TODO: Use `is_res_class_III` instead of `h3_is_res_class_III`
        # While h3-py release 4, `is_res_class_III` is not available.
        return pd.Series(
            self.index.map(method_from_h3(self.index, "h3_is_res_class_III")),
            index=self.index,
        )


    @available_if(is_h3)
    def to_int(self) -> pd.Index:
        """
        Converts an H3 64-bit integer index to a hexadecimal string.

        Returns
        -------
        Index(int64)

        Raises
        ------
        TypeError
            If the dtype of the Index is not string.

        See Also
        --------
        h3.str_to_int
        dtoolkit.geoaccessor.index.h3.to_str

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
        from h3.api.numpy_int import string_to_h3

        if not is_string_dtype(self.index):
            raise TypeError(f"Expected Index(string), but got {self.index.dtype!r}.")
        return self.index.map(string_to_h3)

    @available_if(is_h3)
    def to_str(self) -> pd.Series:
        """
        Converts a hexadecimal string to an H3 64-bit integer index.

        Returns
        -------
        Index(string)

        Raises
        ------
        TypeError
            If the dtype of the Index is not int64.

        See Also
        --------
        h3.int_to_str
        dtoolkit.geoaccessor.index.h3.to_int

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> index = pd.Index([612845052823076863, 614269156845420543])
        Int64Index([612845052823076863, 614269156845420543], dtype='int64')
        >>> index
        >>> index.h3.to_str()
        Index(['88143541bdfffff', '886528b2a3fffff'], dtype='object')
        """
        # TODO: Use `int_to_str` instead of `h3_to_string`
        # While h3-py release 4, `int_to_str` is not available.
        from h3.api.numpy_int import h3_to_string

        if not is_int64_dtype(self.s):
            raise TypeError(f"Expected Index(int64), but got {self.index.dtype!r}.")
        return self.s.apply(h3_to_string)
