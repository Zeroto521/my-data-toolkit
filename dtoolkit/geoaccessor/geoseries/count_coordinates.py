import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
@doc(klass="GeoSeries")
def count_coordinates(s: gpd.GeoSeries, /) -> pd.Series:
    """
    Counts the number of coordinate pairs in each geometry of
    :class:`~geopandas.{klass}`.

    A sugary syntax wraps :meth:`shapely.count_coordinates`.

    Returns
    -------
    Series(int64)

    See Also
    --------
    shapely.count_coordinates
        The core algorithm of this accessor.

    dtoolkit.geoaccessor.geoseries.count_coordinates
        Counts the number of coordinate pairs in each geometry of GeoSeries.

    dtoolkit.geoaccessor.geodataframe.count_coordinates
        Counts the number of coordinate pairs in each geometry of GeoDataFrame.

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import geopandas as gpd
    >>> df = gpd.GeoSeries.from_wkt(
    ...     [
    ...         "POINT (0 0)",
    ...         "LINESTRING (2 2, 4 4)",
    ...         None,
    ...     ],
    ... ).to_frame("geometry")
    >>> df
                                            geometry
    0                        POINT (0.00000 0.00000)
    1  LINESTRING (2.00000 2.00000, 4.00000 4.00000)
    2                                           None
    >>> df.count_coordinates()
    0    1
    1    2
    2    0
    Name: geometry, dtype: int64
    """
    from shapely import count_coordinates

    return s.apply(count_coordinates)
