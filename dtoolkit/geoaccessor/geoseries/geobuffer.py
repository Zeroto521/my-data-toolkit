from __future__ import annotations

from textwrap import dedent

import geopandas as gpd
import numpy as np
import pandas as pd
from pandas.api.types import is_list_like
from pandas.api.types import is_number
from pandas.util._decorators import doc

from dtoolkit._typing import Number
from dtoolkit._typing import OneDimArray
from dtoolkit.accessor.series import getattr  # noqa
from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
@doc(
    klass=":class:`~geopandas.GeoSeries`",
    alias="s",
    examples=dedent(
        """
    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import geopandas as gpd
    >>> from shapely.geometry import Point, LineString
    >>> s = gpd.GeoSeries(
    ...     [
    ...         Point(122, 55),
    ...         Point(100, 1),
    ...         LineString([Point(122, 55), Point(100, 1)])
    ...     ],
    ...     crs="EPSG:4326",
    ... )
    >>> s
    0    POINT (122.00000 55.00000)
    1    POINT (100.00000  1.00000)
    2    LINESTRING (122.00000 55.00000, 100.00000 1.00...
    dtype: geometry
    >>> s.geobuffer(100)
    0    POLYGON ((122.00156 55.00001, 122.00156 54.999...
    1    POLYGON ((100.00090 1.00000, 100.00089 0.99991...
    2    POLYGON ((100.00088 0.99981, 100.00086 0.99972...
    dtype: geometry
    """,
    ),
)
def geobuffer(
    s: gpd.GeoSeries,
    distance: Number | list[Number] | OneDimArray,
    **kwargs,
) -> gpd.GeoSeries:
    """
    Creates geographic buffers for {klass}.

    Reprojects input features into the *UTM* projection, buffers them,
    then reprojects back into the original geographic coordinates.

    Parameters
    ----------
    distance : int, float, list-like of int or float, the unit is meter.
        The radius of the buffer. If :obj:`~numpy.ndarray` or :obj:`~pandas.Series`
        are used then it must have same length as the ``{alias}``.

    Returns
    -------
    {klass}

    See Also
    --------
    dtoolkit.geoaccessor.geoseries.geobuffer
    dtoolkit.geoaccessor.geodataframe.geobuffer
    geopandas.GeoSeries.buffer

    {examples}
    """

    if is_list_like(distance):
        if len(distance) != len(s):
            raise IndexError(
                f"Length of 'distance' doesn't match length of the {type(s)!r}.",
            )

        if isinstance(distance, pd.Series):
            if not s.index.equals(distance.index):
                raise IndexError(
                    "Index values of 'distance' sequence doesn't "
                    f"match index values of the {type(s)!r}",
                )
        else:
            distance = np.asarray(distance)

    elif not is_number(distance):
        raise TypeError("type of 'distance' should be int or float.")

    utms = s.utm_crs().getattr("code").to_numpy()

    s_index = s.index
    s = s.reset_index(drop=True)
    return (
        pd.concat(
            (
                s[utms == utm]
                .to_crs(epsg=utm)
                .buffer(
                    distance[utms == utm] if is_list_like(distance) else distance,
                    **kwargs,
                )
                .to_crs(s.crs)
            )
            if utm is not None
            else s[utms == utm]
            for utm in np.unique(utms)
        )
        .sort_index()
        .set_axis(s_index)
        .rename(s.name)
        .set_crs(s.crs)
    )
