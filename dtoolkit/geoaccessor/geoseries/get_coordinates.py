from textwrap import dedent

import geopandas as gpd
import pandas as pd
import pygeos
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
@doc(
    klass=":class:`~geopandas.GeoSeries`",
    examples=dedent(
        """
    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import geopandas as gpd
    >>> s = gpd.GeoSeries.from_wkt(["POINT (0 0)", "LINESTRING (2 2, 4 4)", None])
    >>> s
    0                          POINT (0.00000 0.00000)
    1    LINESTRING (2.00000 2.00000, 4.00000 4.00000)
    2                                             None
    dtype: geometry
    >>> s.get_coordinates()
    0                [[0.0, 0.0]]
    1    [[2.0, 2.0], [4.0, 4.0]]
    2                          []
    dtype: object
    """,
    ),
)
def get_coordinates(s: gpd.GeoSeries, **kwargs) -> pd.Series:
    """
    Gets coordinates from each geometry of {klass}.

    A sugary syntax wraps :meth:`pygeos.coordinates.get_coordinates`.

    Parameters
    ----------
    **kwargs
        See the documentation for :meth:`pygeos.coordinates.get_coordinates` for
        complete details on the keyword arguments.

    Returns
    -------
    Series

    See Also
    --------
    dtoolkit.geoaccessor.geoseries.get_coordinates
        Gets coordinates from each geometry of GeoSeries.
    dtoolkit.geoaccessor.geodataframe.get_coordinates
        Gets coordinates from each geometry of GeoDataFrame.
    pygeos.coordinates.get_coordinates
        The core algorithm of this accessor.
    {examples}
    """

    return s.apply(
        lambda x: pygeos.get_coordinates(pygeos.from_shapely(x), **kwargs),
    )
