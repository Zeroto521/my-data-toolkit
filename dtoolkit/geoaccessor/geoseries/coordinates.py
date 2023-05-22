import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc
from shapely import get_coordinates

from dtoolkit.geoaccessor.register import register_geoseries_method
from dtoolkit.util._decorator import warning


@register_geoseries_method
@doc(klass="GeoSeries")
@warning(
    "The 'coordinates' is deprecated and will be removed in 0.0.22. "
    "Please use 'GeoSeries.get_coordinates' in geopandas 0.13 instead."
    "(Warning added DToolKit 0.0.21)",
    DeprecationWarning,
    stacklevel=3,
)
def coordinates(s: gpd.GeoSeries, /, **kwargs) -> pd.Series:
    """
    Gets coordinates from each geometry of :class:`~geopandas.{klass}`.

    A sugary syntax wraps :meth:`shapely.get_coordinates`.

    .. deprecated:: 0.0.22
        The 'coordinates' is deprecated.
        Please use 'GeoSeries.get_coordinates' in geopandas 0.13 instead.

    Parameters
    ----------
    **kwargs
        See the documentation for :meth:`shapely.get_coordinates` for
        complete details on the keyword arguments.

    Returns
    -------
    Series

    See Also
    --------
    shapely.get_coordinates
        The core algorithm of this accessor.

    dtoolkit.geoaccessor.geoseries.coordinates
        Gets coordinates from each geometry of GeoSeries.

    dtoolkit.geoaccessor.geodataframe.coordinates
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
    >>> df.coordinates()
    0                [[0.0, 0.0]]
    1    [[2.0, 2.0], [4.0, 4.0]]
    2                          []
    Name: geometry, dtype: object
    """

    return s.apply(get_coordinates, **kwargs)
