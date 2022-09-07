import geopandas as gpd
import pytest
from shapely.geometry import Point

from dtoolkit.geoaccessor.geoseries import geodistance


@pytest.mark.parametrize(
    "s, other, align, error",
    [
        (
            gpd.GeoSeries([Point(122, 55), Point(100, 1)]),
            gpd.GeoSeries([Point(122, 55), Point(100, 1)]),
            True,
            ValueError,
        ),
        (
            gpd.GeoSeries([Point(122, 55), Point(100, 1)], crs=4326),
            None,
            True,
            TypeError,
        ),
        (
            gpd.GeoSeries([Point(122, 55), Point(100, 1)]),
            gpd.GeoSeries([Point(122, 55), Point(100, 1)], crs=4326),
            True,
            ValueError,
        ),
    ],
)
def test_error(s, other, align, error):
    with pytest.raises(error):
        geodistance(s, other, align=align)


def test_warning():
    s1 = gpd.GeoSeries([Point(122, 55), Point(100, 1)], crs=4326)
    s2 = gpd.GeoSeries([Point(120, 30), Point(120, 50)], index=[1, 2], crs=4326)

    with pytest.warns(UserWarning):
        geodistance(s1, s2)
