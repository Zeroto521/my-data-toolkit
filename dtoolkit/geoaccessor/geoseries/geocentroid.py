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
    x, y = coord.mean().tolist()
    for _ in range(max_iter):
        dis = geodistance(s, Point(x, y))
        x_, y_ = (coord.mul(dis, axis=0).sum() / dis.sum()).tolist()

        if abs(x - x_) <= tol and abs(y - y_) <= tol:
            break
        x, y = x_, y_

    return Point(x, y)
