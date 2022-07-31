from typing import Literal

import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.accessor.series import swap_index_values  # noqa: F401
from dtoolkit.geoaccessor.geoseries import count_duplicated_geometry  # noqa: F401
from dtoolkit.geoaccessor.geoseries.count_duplicated_geometry import BINARY_PREDICATE
from dtoolkit.geoaccessor.geoseries.count_duplicated_geometry import self_sjoin
from dtoolkit.geoaccessor.geoseries.count_duplicated_geometry import set_unique_index
from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
@doc()
def duplicated_geometry(
    s: gpd.GeoDataFrame,
    /,
    predicate: BINARY_PREDICATE = "intersects",
    keep: Literal["first", "last", False] = "first",
) -> pd.Series:
    """
    Return boolean Series denoting duplicate geometries.

    Parameters
    ----------
    predicate : {{'intersects', 'crosses', 'overlaps', 'touches', 'covered_by', \
'contains_properly', 'contains', 'within', 'covers'}}, default 'intersects'
        The binary predicate is used to validate whether the geometries are duplicates
        or not.

    keep : {{'first', 'last', False}}, default 'first'
        - ``first`` : Mark duplicates as ``True`` except for the first occurrence.
        - ``last`` : Mark duplicates as ``True`` except for the last occurrence.
        - False : Mark all duplicates as ``True``.

    Returns
    -------
    Series

    See Also
    --------
    geopandas.sjoin
    dtoolkit.geoaccessor.geoseries.duplicated_geometry
    dtoolkit.geoaccessor.geodataframe.duplicated_geometry

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
    >>> df.duplicated_geometry().head()
    1     True
    2     True
    11    True
    12    True
    13    True
    dtype: bool
    """

    return s.iloc[
        s.to_frame("geometry")
        .pipe(set_unique_index, drop=True)
        .pipe(self_sjoin, predicate=predicate)
        .drop_geometry()
        .to_series()
        .pipe(lines_group, len(s))
        .drop_duplicates(keep=keep)
        .index
    ]


def lines_group(s: pd.Series, length: int) -> pd.Series:
    groups = []
    for i, v in s.items():
        for group in groups:
            if i in group or v in group:
                group.update({i, v})
                break
        else:
            groups.append({i, v})

    for i in range(length):
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
        .pipe(swap_index_values)
        .sort_index()
    )
