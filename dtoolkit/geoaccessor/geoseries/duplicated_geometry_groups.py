from typing import Literal

import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc

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
@doc()
def duplicated_geometry_groups(
    s: gpd.GeoSeries,
    /,
    predicate: BINARY_PREDICATE = "intersects",
) -> pd.Series:
    """
    Return boolean Series denoting duplicate geometries.

    Parameters
    ----------
    predicate : {{'intersects', 'crosses', 'overlaps', 'touches', 'covered_by', \
'contains_properly', 'contains', 'within', 'covers'}}, default 'intersects'
        The binary predicate is used to validate whether the geometries are duplicates
        or not.

    Returns
    -------
    Series

    Warnings
    --------
    UserWarning
        If the index of the inputting is not unique.

    See Also
    --------
    geopandas.sjoin
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

    # add misssing group via natural number
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