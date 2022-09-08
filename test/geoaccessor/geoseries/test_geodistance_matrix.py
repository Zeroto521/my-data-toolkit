import geopandas as gpd
import pytest
from shapely.geometry import Point

from dtoolkit.geoaccessor.geoseries import geodistance_matrix


@pytest.mark.parametrize(
    "s, other, error",
    [
        (
            gpd.GeoSeries([Point(120, 30), Point(122, 55), Point(100, 1)]),
            gpd.GeoSeries([Point(120, 30), Point(110, 40)], crs=4326),
            ValueError,
        ),
        (
            gpd.GeoSeries([Point(120, 30), Point(110, 40)], crs=4326),
            gpd.GeoSeries([Point(120, 30), Point(122, 55), Point(100, 1)]),
            ValueError,
        ),
    ],
)
def test_error(s, other, error):
    with pytest.raises(error):
        geodistance_matrix(s, other=other)
