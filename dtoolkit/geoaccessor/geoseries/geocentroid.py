import geopandas as gpd
from shapely import Point

from dtoolkit.geoaccessor.geoseries.geodistance import geodistance
from dtoolkit.geoaccessor.geoseries.xy import xy
from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
def geocentroid(s: gpd.GeoSeries, /, max_iter: int = 300, tol: float = 1e-4) -> Point:
    if s.crs != 4326:
        raise ValueError(f"Only support 'EPSG:4326' CRS, but got {s.crs!r}.")
    if not all(s.geom_type == "Point"):
        raise TypeError("Only support 'Point' geometry type.")

    coord = xy(s)
    X = coord.mean()
    for _ in range(max_iter):
        dis = geodistance(s, Point(*X.tolist()))
        Xt = coord.mul(dis, axis=0).sum() / dis.sum()

        if ((X - Xt).abs() <= tol).all():
            break

        X = Xt

    return Point(*X.tolist())
