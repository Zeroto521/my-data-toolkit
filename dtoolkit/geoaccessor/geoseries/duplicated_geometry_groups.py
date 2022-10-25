from typing import Literal

import geopandas as gpd
import pandas as pd

from dtoolkit.accessor.series import set_unique_index  # noqa: F401
from dtoolkit.accessor.series import swap_index_values  # noqa: F401
from dtoolkit.geoaccessor.register import register_geoseries_method


BINARY_PREDICATE = Literal[
    "intersects",
    "crosses",
    "overlaps",
    "touches",
    "covered_by",
    "contains_properly",
    "contains",
    "within",
    "covers",
]


@register_geoseries_method
def duplicated_geometry_groups(
    s: gpd.GeoSeries,
    /,
    predicate: BINARY_PREDICATE = "intersects",
) -> pd.Series:
    """
    Labels of duplicate geometries.

    Parameters
    ----------
    predicate : {'intersects', 'crosses', 'overlaps', 'touches', 'covered_by', \
'contains_properly', 'contains', 'within', 'covers'}, default 'intersects'
        The binary predicate is used to validate whether the geometries are duplicates
        or not.

    Returns
    -------
    Series
        ``index`` is the index of inputting, ``values`` is the labels of groups.
        And labels are natural numbers.

    Warns
    -----
    UserWarning
        If the index of the inputting is not unique.

    See Also
    --------
    geopandas.sjoin
    dtoolkit.geoaccessor.geoseries.duplicated_geometry
    dtoolkit.geoaccessor.geoseries.duplicated_geometry_groups
    dtoolkit.geoaccessor.geodataframe.duplicated_geometry
    dtoolkit.geoaccessor.geodataframe.duplicated_geometry_groups

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import geopandas as gpd
    >>> from shapely.geometry import Polygon
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

    - 0 and 1 are intersecting.
    - 1 and 2 are intersecting.
    - 3 is alone.

    So there are two groups: ``(0, 1, 2)`` and ``(3,)``.

    >>> df.duplicated_geometry_groups()
    0    0
    1    0
    2    0
    3    1
    dtype: int64
    """

    # NOTE: `predicate` requires geopandas >= 0.10.0
    return (
        s.to_frame("geometry")
        .set_unique_index(drop=True)
        .pipe(self_sjoin, predicate=predicate)
        .drop_geometry()
        .to_series()
        .pipe(group_shared_xy, size=s.size)
        .set_axis(s.index)
    )


def self_sjoin(df: gpd.GeoDataFrame, /, **kwargs) -> gpd.GeoDataFrame:
    """
    Perform self-sjoin on a GeoDataFrame.

    Parameters
    ----------
    **kwargs
        See the documentation for :meth:`~geopandas.sjoin` for complete
        details on the keyword arguments except ``left_df`` and ``right_df``.

    Returns
    -------
    GeoDataFrame

    See Also
    --------
    geopandas.sjoin

    Notes
    -----
    ``left_df`` and ``right_df`` parameter are ``df`` and can't be overridden.
    """

    return gpd.sjoin(df, df, **kwargs)


def group_shared_xy(s: pd.Series, /, size: int) -> pd.Series:
    """
    Group the shared 'x' and 'y' coordinates.

    A simple example::

        # group x-y relationship

        # diagonal matrix in logical
        #    0  1  2  3
        # 0  √
        # 1     √  √
        # 2     √  √  √
        # 3        √  √

        # which data in real
        [
            (1, 2),  # or `(2, 1)`
            (2, 3),  # or `(3, 2)`
        ]

        # into

        [
            {0},
            {1, 2, 3},
        ]

    Parameters
    ----------
    s : Series
        Its index is the 'x' and values is the 'y'. Require all 'x' value is not equal
        to 'y' value 'x-y' (or 'y-x') parts.

    size : int
        The size of the matrix.

    Returns
    -------
    Series
        index is the original ``index``, ``values`` is the label of group.

    Notes
    -----
    - Only support 2d coordinates, it means data unit is ``(x, y)``.
    - Only support 'diagonal maxtrix', it means 'x' value equal to 'y' value.
    - Only support natural numbers of labels.

    Examples
    --------
    >>> import pandas as pd
    >>> s = pd.Series([2, 3], name='y', index=pd.Index([1, 2], name='x'))
    >>> s
    x
    1    2
    2    3
    Name: y, dtype: int64
    >>> group_shared_xy(s, 4)
    0    1
    1    0
    2    0
    3    0
    dtype: int64
    """

    groups = []
    for x, y in s.items():
        for group in groups:
            if x in group or y in group:
                group.update({x, y})
                break
        else:
            groups.append({x, y})

    # add missing group via natural number
    for i in range(size):
        for group in groups:
            if i in group:
                break
        else:
            groups.append({i})

    return pd.Series(groups).explode().swap_index_values().sort_index()
