from __future__ import annotations

from typing import Literal

import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc

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
@doc(klass=":class:`~geopandas.GeoSeries`")
def count_duplicated_geometry(
    s: gpd.GeoSeries,
    /,
    predicate: BINARY_PREDICATE = "intersects",
) -> pd.Series:
    """
    Count the number of duplicated geometries in a {klass}.

    Parameters
    ----------
    predicate : {{'intersects', 'crosses', 'overlaps', 'touches', 'covered_by', \
'contains_properly', 'contains', 'within', 'covers'}}, default 'intersects'
        The binary predicate is used to validate whether the geometries are duplicates
        or not.

    Returns
    -------
    Series

    See Also
    --------
    geopandas.sjoin
    dtoolkit.geoaccessor.geoseries.count_duplicated_geometry
    dtoolkit.geoaccessor.geodataframe.count_duplicated_geometry

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import geopandas as gpd
    >>> df = (
    ...     gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    ...     .query('continent == "Africa"')
    ... )
    >>> df.head()  # doctest: +SKIP
         pop_est  ...                                           geometry
    1   53950935  ...  POLYGON ((33.90371 -0.95000, 34.07262 -1.05982...
    2     603253  ...  POLYGON ((-8.66559 27.65643, -8.66512 27.58948...
    11  83301151  ...  POLYGON ((29.34000 -4.49998, 29.51999 -5.41998...
    12   7531386  ...  POLYGON ((41.58513 -1.68325, 40.99300 -0.85829...
    13  47615739  ...  POLYGON ((39.20222 -4.67677, 37.76690 -3.67712...
    <BLANKLINE>
    [5 rows x 6 columns]
    >>> df.count_duplicated_geometry().head()
    1      8
    2      3
    11     9
    12     3
    13     5
    dtype: int64
    """

    return (
        s.to_frame("geometry")
        .pipe(set_unique_index, drop=True)
        .pipe(self_sjoin, predicate=predicate)
        .groupby_index()
        .geometry.count()
        .set_axis(s.index)  # Restore original index
        .rename(None)
        .__sub__(1)  # 1 means itself sjoin, but doesn't sjoin other geometries
    )


def set_unique_index(df: pd.DataFrame, /, **kwargs) -> pd.DataFrame | pd.Series:
    """
    Set unique index via ``.reset_index`` if ``df.index`` isn't unique.

    Parameters
    ----------
    **kwargs
        See the documentation for :meth:`~pandas.DataFrame.set_index` or
        :meth:`~pandas.Series.set_index` for complete details on the keyword arguments.

    Returns
    -------
    DataFrame or Series
        DataFrame if ``df`` is a DataFrame, Series if ``df`` is a Series.

    See Also
    --------
    pandas.Series.reset_index
    pandas.DataFrame.reset_index
    """

    if not df.index.is_unique:
        from warnings import warn

        warn(f"The 'Index' of {type(df)} is not unique.")
        return df.reset_index(**kwargs)

    return df


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
