import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
@doc(klass="GeoSeries")
def get_coordinates(s: gpd.GeoSeries, /, **kwargs) -> pd.Series:
    """
    Gets coordinates from each geometry of :class:`~geopandas.{klass}`.

    A sugary syntax wraps :meth:`pygeos.coordinates.get_coordinates`.

    Parameters
    ----------
    **kwargs
        See the documentation for :meth:`pygeos.coordinates.get_coordinates` for
        complete details on the keyword arguments.

    Returns
    -------
    Series

    Raises
    ------
    ModuleNotFoundError
        If don't have module named 'pygeos'.

    See Also
    --------
    pygeos.coordinates.get_coordinates
        The core algorithm of this accessor.

    dtoolkit.geoaccessor.geoseries.get_coordinates
        Gets coordinates from each geometry of GeoSeries.

    dtoolkit.geoaccessor.geodataframe.get_coordinates
        Gets coordinates from each geometry of GeoDataFrame.

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
    >>> df.get_coordinates()
    0                [[0.0, 0.0]]
    1    [[2.0, 2.0], [4.0, 4.0]]
    2                          []
    Name: geometry, dtype: object
    """
    from pygeos import from_shapely, get_coordinates

    return s.apply(lambda x: get_coordinates(from_shapely(x), **kwargs))
