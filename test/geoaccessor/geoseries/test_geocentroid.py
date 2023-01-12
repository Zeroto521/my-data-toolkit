import geopandas as gpd
from shapely import Point

from dtoolkit.geoaccessor.geoseries import geocentroid


def test_one_point():
    s = gpd.GeoSeries(Point(100, 32), crs=4326)

    assert geocentroid(s) == Point(100, 32)
