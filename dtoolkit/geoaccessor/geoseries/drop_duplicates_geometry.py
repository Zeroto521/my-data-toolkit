from typing import Literal

import geopandas as gpd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.geoseries.duplicated_geometry import duplicated_geometry
from dtoolkit.geoaccessor.geoseries.duplicated_geometry_groups import BINARY_PREDICATE
from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
@doc(klass="GeoSeries")
def drop_duplicates_geometry(
    s: gpd.GeoSeries,
    /,
    predicate: BINARY_PREDICATE = "intersects",
    keep: Literal["first", "last", False] = "first",
) -> gpd.GeoSeries:
    """
    Remove duplicate geometry rows.

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
    {klass}

    See Also
    --------
    geopandas.sjoin
    dtoolkit.geoaccessor.geoseries.duplicated_geometry
    dtoolkit.geoaccessor.geoseries.drop_duplicates_geometry
    dtoolkit.geoaccessor.geodataframe.duplicated_geometry
    dtoolkit.geoaccessor.geodataframe.drop_duplicates_geometry

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

    Work for GeoSeries.

    >>> df.geometry.drop_duplicates_geometry()
    0    POLYGON ((0.00000 0.00000, 1.00000 0.00000, 1....
    3    POLYGON ((2.00000 0.00000, 3.00000 0.00000, 3....
    Name: geometry, dtype: geometry

    Work for GeoDataFrame too.

    >>> df.drop_duplicates_geometry()
                                                geometry
    0  POLYGON ((0.00000 0.00000, 1.00000 0.00000, 1....
    3  POLYGON ((2.00000 0.00000, 3.00000 0.00000, 3....
    """

    return s[~duplicated_geometry(s, predicate=predicate, keep=keep)]
