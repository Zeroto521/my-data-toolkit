import geopandas as gpd
import pytest
from shapely import Point

from dtoolkit.geoaccessor.geoseries import geocentroid


@pytest.mark.parametrize(
    "s, error",
    [
        (
            gpd.GeoSeries(
                [
                    Point(100, 32),
                    Point(120, 50),
                    Point(122, 55),
                ],
            ),
            ValueError,
        ),
    ],
)
def test_error(s, error):
    with pytest.raises(error):
        geocentroid(s)


def test_tol():
    # test `tol` parameter
    result = gpd.GeoSeries([Point(100, 50), Point(120, 50)], crs=4326).geocentroid()

    assert result.equals(Point(110, 50))
