import geopandas as gpd
import pytest
from shapely import LineString
from shapely import Point

from dtoolkit.geoaccessor.geoseries import voronoi


@pytest.mark.parametrize(
    "s, error",
    [
        (
            gpd.GeoSeries([Point(122, 55), Point(100, 1)]),
            IndexError,
        ),
        (
            gpd.GeoSeries([Point(122, 55)]),
            IndexError,
        ),
        (
            gpd.GeoSeries(),
            IndexError,
        ),
        (
            gpd.GeoSeries([LineString([(122, 55), (100, 1)])]),
            TypeError,
        ),
    ],
)
def test_error(s, error):
    with pytest.raises(error):
        voronoi(s)
