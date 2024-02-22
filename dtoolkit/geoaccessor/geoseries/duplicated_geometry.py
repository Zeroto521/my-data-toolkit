from __future__ import annotations

from typing import Literal

import geopandas as gpd
import pandas as pd

from dtoolkit.geoaccessor.geoseries.duplicated_geometry_groups import BINARY_PREDICATE
from dtoolkit.geoaccessor.geoseries.duplicated_geometry_groups import (
    duplicated_geometry_groups,
)
from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
def duplicated_geometry(
    s: gpd.GeoDataFrame,
    /,
    predicate: BINARY_PREDICATE | None = None,
    keep: Literal["first", "last", False] = "first",
) -> pd.Series:
    """
    Return boolean Series denoting duplicate geometries.

    Parameters
    ----------
    predicate : {'intersects', 'crosses', 'overlaps', 'touches', 'covered_by', \
'contains_properly', 'contains', 'within', 'covers', None}, default None
        The binary predicate is used to validate whether the geometries are duplicates
        or not. If None, the geometries will directly compares via value relation
        instead of the spatial relation.

        .. versionchanged:: 0.0.19
            The 'predicate' default value is changed from 'intersects' to None.

    keep : {'first', 'last', False}, default 'first'
        - ``first`` : Mark duplicates as ``True`` except for the first occurrence.
        - ``last`` : Mark duplicates as ``True`` except for the last occurrence.
        - False : Mark all duplicates as ``True``.

    Returns
    -------
    Series(bool)

    See Also
    --------
    pandas.Series.duplicated
    geopandas.sjoin
    dtoolkit.geoaccessor.geoseries.duplicated_geometry
    dtoolkit.geoaccessor.geodataframe.duplicated_geometry

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import geopandas as gpd

    Drop duplicated geometries by value equal.

    >>> from shapely import Point
    >>> df = gpd.GeoDataFrame(geometry=[Point(0, 0), Point(0, 0), Point(1, 1)])
    >>> df
                      geometry
    0  POINT (0.00000 0.00000)
    1  POINT (0.00000 0.00000)
    2  POINT (1.00000 1.00000)
    >>> df.duplicated_geometry()
    0    False
    1     True
    2    False
    Name: geometry, dtype: bool

    Drop duplicated geometries by sptial relation.

    >>> from shapely import Polygon
    >>> df = gpd.GeoDataFrame(
    ...     geometry=[
    ...         Polygon([(0,0), (1,0), (1,1), (0,1)]),
    ...         Polygon([(1,1), (2,1), (2,2), (1,2)]),
    ...         Polygon([(2,2), (3,2), (3,3), (2,3)]),
    ...         Polygon([(2, 0), (3, 0), (3, 1)]),
    ...     ],
    ... )
    >>> df
                                                geometry
    0  POLYGON ((0.00000 0.00000, 1.00000 0.00000, 1....
    1  POLYGON ((1.00000 1.00000, 2.00000 1.00000, 2....
    2  POLYGON ((2.00000 2.00000, 3.00000 2.00000, 3....
    3  POLYGON ((2.00000 0.00000, 3.00000 0.00000, 3....
    >>> df.duplicated_geometry('intersects')
    0    False
    1     True
    2     True
    3    False
    dtype: bool
    """

    if predicate is not None:
        s = duplicated_geometry_groups(s, predicate=predicate)
    return s.duplicated(keep=keep)
