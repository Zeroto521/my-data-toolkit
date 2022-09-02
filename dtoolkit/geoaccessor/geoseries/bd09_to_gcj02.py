import geopandas as gpd
import numpy
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
