from typing import Literal

import geopandas as gpd
import pandas as pd

from dtoolkit._typing import SeriesOrFrame
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
    dtoolkit.geoaccessor.geoseries.duplicated_geometry_groups
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

    return (
        s.to_frame("geometry")
        .pipe(set_unique_index, drop=True)
        .pipe(self_sjoin, predicate=predicate)
        .drop_geometry()
        .to_series()
        .pipe(group_shared_xy, index=s.index)
    )


def set_unique_index(data: SeriesOrFrame, /, **kwargs) -> SeriesOrFrame:
    """
    Set unique index via ``.reset_index`` if ``data.index`` isn't unique.

    Parameters
    ----------
    **kwargs
        See the documentation for ``set_index`` for complete details on the keyword
        arguments.

    Returns
    -------
    DataFrame or Series
        Return DataFrame if ``data`` is a DataFrame, else Series.

    See Also
    --------
    pandas.Series.reset_index
    pandas.DataFrame.reset_index
    """

    if not data.index.is_unique:
        from warnings import warn

        warn(
            f"The 'Index' of {type(data).__name__!r} is not unique.",
            stacklevel=6,
        )
        return data.reset_index(**kwargs)

    return data


def self_sjoin(df: gpd.GeoDataFrame, /, **kwargs) -> gpd.GeoDataFrame:
    """
    Perform self-sjoin on a GeoDataFrame.

    Parameters
    ----------
    **kwargs
        See the documentation for :meth:`~geopandas.GeoDataFrame.sjoin` for complete
        details on the keyword arguments except ``left_df`` and ``right_df``.

    Returns
    -------
    GeoDataFrame

    See Also
    --------
    geopandas.GeoDataFrame.sjoin

    Notes
    -----
    ``left_df`` and ``right_df`` parameter are ``df`` and can't be overridden.
    """

    return gpd.sjoin(df, df, **kwargs)


def group_shared_xy(s: pd.Series, index: pd.Index) -> pd.Series:
    """
    Group the shared 'x' and 'y' coordinates.

    A simple example::

        # group x-y relationship
        # diagonal matrix in logical
           0  1  2  3
        0  √
        1     √  √
        2     √  √
        3           √

        # data in real
        [
            (1, 2),
            (2, 3),
        ]

        # into

        [
            (0,),
            (1, 2, 3),
        ]

    Parameters
    ----------
    s : Series
        index is the x, values is the y.

    index : Index
        The original index.

    Returns
    -------
    Series
        index is the original ``index``, ``values`` is the label of group.

    Notes
    -----
    - Only support 2d coordinates, it means data unit is ``(x, y)``.
    - Only support 'diagonal maxtrix', it means 'x valeus equal to 'y' values.
    - Only support natural numbers of labels.
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
    for i in range(len(index)):
        for group in groups:
            if i in group:
                break
        else:
            groups.append({i})

    return (
        pd.Series(
            groups,
        )
        .explode()
        .swap_index_values()
        .sort_index()
        .set_axis(index)
    )
