from __future__ import annotations

from warnings import catch_warnings
from warnings import simplefilter

import geopandas as gpd
import numpy as np
import pandas as pd
from pandas.api.types import is_list_like
from pandas.api.types import is_number
from pandas.util._decorators import doc

from dtoolkit._typing import Number
from dtoolkit._typing import OneDimArray
from dtoolkit.geoaccessor.geoseries.xy import xy  # noqa: F401
from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
@doc(klass="GeoSeries", alias="s")
def geobuffer(
    s: gpd.GeoSeries,
    distance: Number | list[Number] | OneDimArray,
    /,
    **kwargs,
) -> gpd.GeoSeries:
    """
    Creates geographic buffers for :class:`~geopandas.{klass}`.

    Reprojects input features into the *UTM* projection, buffers them,
    then reprojects back into the original geographic coordinates.

    Parameters
    ----------
    distance : int, float, list-like of int or float, the unit is meter.
        The radius of the buffer. If numpy.ndarray or Series are used then it must have
        same length as the ``{alias}``. For ``GeoDataFrame.geobuffer``, it would use the
        column name as the distance prior.

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
    ValueError
        Requires the CRS of the inputting is WGS84 (epsg:4326).

    TypeError
        If ``distance`` is not a number.

    IndexError
        - If ``distance`` is a list-like but its length does not match the length of
         ``{alias}``.
        - If ``distance`` is a Series but its index does not match the index of
         ``{alias}``.

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
    ...              "distance": [0, 10],
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
       distance              where                    geometry
    0         0   close to equator  POINT (122.00000 55.00000)
    1        10  away from equator   POINT (100.00000 1.00000)
    >>> df.geobuffer(100)
       distance  ...                                           geometry
    0         0  ...  POLYGON ((122.00156 55.00001, 122.00156 54.999...
    1        10  ...  POLYGON ((100.00090 1.00000, 100.00089 0.99991...
    <BLANKLINE>
    [2 rows x 3 columns]

    For GeoDataFrame, it could use the column name as the distance to generate buffer.

    >>> df.geobuffer("distance")
       distance  ...                                           geometry
    0         0  ...                                      POLYGON EMPTY
    1        10  ...  POLYGON ((100.00009 1.00000, 100.00009 0.99999...
    <BLANKLINE>
    [2 rows x 3 columns]
    """

    if s.crs != 4326:
        raise ValueError(
            f"The CRS is {s.crs}, which requires is 'WGS86' (EPSG:4326).",
        )

    distance_is_list = is_list_like(distance)
    if not (is_number(distance) or distance_is_list):
        raise TypeError(
            "'distance' should be a number or a list of number, "
            f"but got {type(distance)!r}.",
        )

    if isinstance(distance, pd.Series) and not s.index.equals(distance.index):
        raise IndexError(
            "Index values of 'distance' sequence doesn't "
            f"match index values of the {type(s)!r}",
        )

    if distance_is_list:
        distance = np.asarray(distance)
        if distance.size != s.size:
            raise IndexError(
                f"Length of 'distance' doesn't match length of the {type(s)!r}.",
            )

    with catch_warnings():
        # Ignore UserWarning ("Geometry is in a geographic CRS")
        simplefilter("ignore", UserWarning)
        utms = s.centroid.xy().apply(wgs_to_utm).to_numpy()

    s = s.copy()
    for utm in pd.unique(utms):
        if utm is None:
            continue

        mask = utms == utm
        dis = distance[mask] if distance_is_list else distance
        s[mask] = s[mask].to_crs(utm).buffer(dis, **kwargs).to_crs(4326)

    return s


def wgs_to_utm(point: tuple[float, float]) -> str | None:
    """Based on (x, y), return the best UTM EPSG code."""

    x, y = point
    if is_number(x) and -180 <= x <= 180 and is_number(y) and -90 <= y <= 90:
        zone = (x + 180) // 6 % 60 + 1
        return f"EPSG:{326 if y >= 0 else 327}{zone:02.0f}"
