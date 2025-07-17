import geopandas as gpd
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from shapely import Point

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
        (
            gpd.GeoSeries([Point(120, 30), Point(110, 40)], crs=4326),
            Point(1, 1),
            TypeError,
        ),
        (
            gpd.GeoSeries([Point(120, 30), Point(110, 40)], crs=4326),
            "string",
            TypeError,
        ),
    ],
)
def test_error(s, other, error):
    with pytest.raises(error):
        geodistance_matrix(s, other=other)


def test_geodataframe():
    s = gpd.GeoSeries([Point(122, 55), Point(100, 1)], crs=4326)
    df = gpd.GeoSeries([Point(122, 55), Point(100, 1)], crs=4326).to_frame("geometry")

    assert isinstance(df, gpd.GeoDataFrame)
    result = s.geodistance_matrix(df) / 1e6
    expected = pd.DataFrame([[0, 6.3275778074520295], [6.3275778074520295, 0]])

    assert_frame_equal(result, expected)


def test_none():
    s = gpd.GeoSeries([Point(122, 55), Point(100, 1)], crs=4326)

    result = s.geodistance_matrix()
    expected = pd.DataFrame([[0, 6327577.80745203], [6327577.80745203, 0]])

    assert_frame_equal(result, expected)
