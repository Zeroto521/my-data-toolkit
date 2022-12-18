import geopandas as gpd
import pytest
from shapely.geometry import LineString
from shapely.geometry import Point

from dtoolkit.geoaccessor.geoseries import to_h3


pytest.importorskip("h3")


@pytest.mark.parametrize(
    "s, resolution, drop, name, error",
    [
        # crs != 4326
        (
            gpd.GeoSeries([Point(122, 55), Point(100, 1)]),
            8,
            True,
            None,
            ValueError,
        ),
        # s.name is None and name is None
        (
            gpd.GeoSeries([Point(122, 55), Point(100, 1)], crs=4326),
            8,
            False,
            None,
            ValueError,
        ),
        # geometry type is not Point or Polygon
        (
            gpd.GeoSeries([LineString([(122, 55), (100, 1)])], crs=4326),
            8,
            True,
            None,
            TypeError,
        ),
    ],
)
def test_error(s, resolution, drop, name, error):
    with pytest.raises(error):
        to_h3(s, resolution=resolution, drop=drop, name=name)
