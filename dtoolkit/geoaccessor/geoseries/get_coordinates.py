from __future__ import annotations

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
def get_coordinates(
    s: gpd.GeoSeries,
    include_z: bool = False,
    return_index: bool = False,
) -> pd.Series:
    """
    Gets coordinates from each geometry of {klass}.

    Parameters
    ----------
    include_zbool: bool, default False
        If True include the third dimension in the output.
        If geometry has no third dimension, the z-coordinates will be `NaN`.

    return_index: bool, default False
        If True also return the index of each returned geometry.
        For multidimensional, this indexes into the flattened array
        (in C contiguous order).

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
        lambda x: pygeos.get_coordinates(
            pygeos.from_shapely(x),
            include_z=include_z,
            return_index=return_index,
        ),
    )
