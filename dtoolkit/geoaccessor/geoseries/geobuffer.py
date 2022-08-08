from __future__ import annotations

from warnings import catch_warnings
from warnings import simplefilter
from warnings import warn

import geopandas as gpd
import numpy as np
import pandas as pd
from pandas.api.types import is_list_like
from pandas.api.types import is_number
from pandas.util._decorators import doc

from dtoolkit._typing import Number
from dtoolkit._typing import OneDimArray
from dtoolkit.accessor.series import set_unique_index
from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
@doc(klass=":class:`~geopandas.GeoSeries`", alias="s")
def geobuffer(
    s: gpd.GeoSeries,
    distance: Number | list[Number] | OneDimArray,
    /,
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

    Warns
    -----
    UserWarning
        - If the index of the inputting is not unique.
        - If the CRS of the inputting is not WGS84 (epsg:4326).

    Raises
    ------
    IndexError
        - If ``distance`` is a list-like but its length does not match the length of
         ``{alias}``.
        - If ``distance`` is a Series but its index does not match the index of
         ``{alias}``.
    TypeError
        If ``distance`` is not a number.

    See Also
    --------
    geopandas.GeoSeries.buffer
    dtoolkit.geoaccessor.geoseries.geobuffer
    dtoolkit.geoaccessor.geodataframe.geobuffer

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd
    >>> df = (
    ...      pd.DataFrame(
    ...          {{
    ...              "where": ["close to equator", "away from equator"],
    ...              "x": [122, 100],
    ...              "y": [55, 1],
    ...          }},
    ...      )
    ...      .from_xy(
    ...          "x",
    ...          "y",
    ...          crs=4326,
    ...          drop=True,
    ...     )
    ... )
    >>> df
                   where                    geometry
    0   close to equator  POINT (122.00000 55.00000)
    1  away from equator   POINT (100.00000 1.00000)
    >>> df.geobuffer(100)
                   where                                           geometry
    0   close to equator  POLYGON ((122.00156 55.00001, 122.00156 54.999...
    1  away from equator  POLYGON ((100.00090 1.00000, 100.00089 0.99991...
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

    s_index = s.index
    s = set_unique_index(s, drop=True)

    crs = s.crs
    if s.crs != 4326:
        warn(
            f"The CRS is {s.crs}, which requires is 'WGS86' (EPSG:4326).",
            stacklevel=3,
        )
        s = s.to_crs(4326)

    with catch_warnings():
        # Ignore UserWarning ("Geometry is in a geographic CRS")
        simplefilter("ignore", UserWarning)
        utms = s.centroid.apply(
            lambda p: (wgs_to_utm(p.x, p.y) if p else None),
        ).to_numpy()

    return (
        pd.concat(
            (
                s[utms == utm]
                .to_crs(utm)
                .buffer(
                    distance[utms == utm] if is_list_like(distance) else distance,
                    **kwargs,
                )
                .to_crs(crs)
            )
            if isinstance(utm, str)
            else s[pd.isnull(utms)]
            for utm in pd.unique(utms)
        )
        .sort_index()
        .set_axis(s_index)
        .rename(s.name)
    )


def wgs_to_utm(lon: float, lat: float) -> str | None:
    """Based on `(lat, lng)`, return the best UTM EPSG code."""

    if is_number(lon) and is_number(lat) and -180 <= lon <= 180 and -90 <= lat <= 90:
        zone = (lon + 180) // 6 % 60 + 1
        return f"EPSG:{326 if lat >= 0 else 327}{zone:02.0f}"
