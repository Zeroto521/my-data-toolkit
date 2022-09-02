import geopandas as gpd
import numpy as np
from pandas.util._decorators import doc

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

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd
    >>> df = pd.DataFrame(
    ...     {{
    ...         "x": [114.21892734521, 128.543],
    ...         "y": [29.575429778924, 37.065],
    ...     }},
    ...     index=[2, 0],
    ... )
    >>> df
                x         y
    2  114.218927  29.57543
    0  128.543000  37.06500
    >>> df.bd09_to_gcj02()
    2    POINT (114.21243 29.56938)
    0    POINT (128.53659 37.05875)
    """

    if s.crs != 4326:
        raise ValueError(f"Only support 'EPSG:4326' CRS, but got {s.crs!r}.")

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
