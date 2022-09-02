import geopandas as gpd
import numpy as np
import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.accessor.series import set_unique_index
from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
@doc(klass="GeoSeries")
def bd09_to_gcj02(s: gpd.GeoSeries, /) -> gpd.GeoSeries:
    """
    China web map CRS transformer, ``BD-09`` to ``GCJ-02``.

    Returns
    -------
    {klass}
        Replaced original geometry.

    Raises
    ------
    ValueError
        If the CRS is not ``ESGP:4326``.

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd
    >>> df = pd.DataFrame(
    ...     {{
    ...         "x": [114.21892734521, 128.543, 1],
    ...         "y": [29.575429778924, 37.065, 1],
    ...     }},
    ...     index=[2, 0, 1],
    ... )
    >>> df
                x         y
    2  114.218927  29.57543
    0  128.543000  37.06500
    1    1.000000   1.00000
    >>> df.bd09_to_gcj02()
    2    POINT (114.21243 29.56938)
    0    POINT (128.53659 37.05875)
    1       POINT (1.00000 1.00000)
    """
    if s.crs != 4326:
        raise ValueError(f"Only support 'EPSG:4326' CRS, but got {s.crs!r}.")

    s_index = s.index
    s = set_unique_index(s, drop=True)
    mask = is_in_china(s).to_numpy()
    return (
        pd.concat((s[~mask], _bd09_to_gcj02(s[mask])))
        .sort_index()
        .set_axis(s_index)
        .rename(s.name)
    )


def is_in_china(s: gpd.GeoSeries, /) -> pd.Series:
    """
    Based on China boundary to judge whether a point is in China.

    Parameters
    ----------
    GeoSeries
        The ESGP:4326 coordinates of the point.

    Returns
    -------
    Series of bool
    """
    from shapely.geometry import box

    return s.covered_by(box(73.66, 3.86, 135.05, 53.55))


def _bd09_to_gcj02(s: gpd.GeoSeries, /) -> gpd.GeoSeries:
    pi = np.pi * 3000 / 180

    x = s.x - 0.0065
    y = s.y - 0.006
    z = np.sqrt(x * x + y * y) - 2e-5 * np.sin(y * pi)

    theta = np.arctan2(y, x) - 3e-6 * np.cos(x * pi)
    return gpd.GeoSeries(
        gpd.points_from_xy(
            x=z * np.cos(theta),
            y=z * np.sin(theta),
        ),
        index=s.index,
        crs=s.crs,
    )
