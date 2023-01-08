import geopandas as gpd
from shapely import Point

from dtoolkit.geoaccessor.geoseries import geocentroid  # noqa: F401


def test_tol():
    result = gpd.GeoSeries([Point(100, 50), Point(120, 50)], crs=4326).geocentroid()

    assert result.equals(Point(110, 50))
