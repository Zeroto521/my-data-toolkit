import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
@doc(klass=":class:`~geopandas.GeoSeries`")
def count_coordinates(s: gpd.GeoSeries, /) -> pd.Series:
    """
    Counts the number of coordinate pairs in each geometry of {klass}.

    A sugary syntax wraps :meth:`pygeos.coordinates.count_coordinates`.

    Returns
    -------
    Series

    Raises
    ------
    ModuleNotFoundError
        If don't have module named 'pygeos'.

    See Also
    --------
    dtoolkit.geoaccessor.geoseries.count_coordinates
        Counts the number of coordinate pairs in each geometry of GeoSeries.

    dtoolkit.geoaccessor.geodataframe.count_coordinates
        Counts the number of coordinate pairs in each geometry of GeoDataFrame.

    pygeos.coordinates.count_coordinates
        The core algorithm of this accessor.

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import geopandas as gpd
    >>> dF = gpd.GeoSeries.from_wkt(
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
    from pygeos import count_coordinates, from_shapely

    return s.apply(lambda x: count_coordinates(from_shapely(x)))
