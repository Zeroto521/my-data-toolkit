import geopandas as gpd
from shapely import Point

import pytest

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
                ]
            ),
            ValueError,
        ),
    ],
)
def test_error(s, error):
    with pytest.raises(error):
        geocentroid(s)
