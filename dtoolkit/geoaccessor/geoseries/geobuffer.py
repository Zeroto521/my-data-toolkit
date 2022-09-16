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
from dtoolkit.accessor.series import set_unique_index
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

    ValueError
        Requires the CRS of the inputting is WGS84 (epsg:4326).

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
    if s.crs != 4326:
        raise ValueError(
            f"The CRS is {s.crs}, which requires is 'WGS86' (EPSG:4326).",
        )

    if is_number(distance):
        ...
    elif is_list_like(distance):
        if len(distance) != s.size:
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
    else:
        raise TypeError(
            "'distance' should be a number or a list of number, "
            f"but got {type(distance)!r}."
        )

    s_index = s.index
    s = set_unique_index(s, drop=True)

    with catch_warnings():
        # Ignore UserWarning ("Geometry is in a geographic CRS")
        simplefilter("ignore", UserWarning)
        utms = s.centroid.xy().apply(wgs_to_utm).to_numpy()

    return (
        pd.concat(
            _geobuffer(
                s[utms == utm],
                distance[utms == utm] if is_list_like(distance) else distance,
                utm,
                **kwargs,
            )
            if isinstance(utm, str)
            else s[pd.isnull(utms)]
            for utm in pd.unique(utms)
        )
        .sort_index()
        .set_axis(s_index)
        .rename(s.name)
    )


def wgs_to_utm(point: tuple[float, float]) -> str | None:
    """Based on (x, y), return the best UTM EPSG code."""

    x, y = point
    if is_number(x) and -180 <= x <= 180 and is_number(y) and -90 <= y <= 90:
        zone = (x + 180) // 6 % 60 + 1
        return f"EPSG:{326 if y >= 0 else 327}{zone:02.0f}"


def _geobuffer(s: gpd.GeoSeries, distance, to_crs, **kwargs):
    return (
        s.to_crs(to_crs)
        .buffer(
            distance,
            **kwargs,
        )
        .to_crs(s.crs)
    )
