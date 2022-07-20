import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.geoseries import count_duplicated_geometry  # noqa: F401
from dtoolkit.geoaccessor.geoseries.count_duplicated_geometry import BINARY_PREDICATE
from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
@doc()
def duplicated_geometry(
    s: gpd.GeoDataFrame,
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

    return s.count_duplicated_geometry(predicate=predicate) >= 1
