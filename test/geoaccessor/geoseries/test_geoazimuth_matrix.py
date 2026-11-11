import geopandas as gpd
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from shapely import Point

from dtoolkit.geoaccessor.geoseries import geoazimuth_matrix


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
        geoazimuth_matrix(s, other=other)


def test_pair_matrix():
    s = gpd.GeoSeries([Point(116.4, 39.9), Point(121.5, 31.2)], crs=4326)
    other = gpd.GeoSeries([Point(120, 30), Point(110, 40)], crs=4326)

    result = s.geoazimuth_matrix(other)
    expected = pd.DataFrame(
        [
            [162.34309829667646, 273.22246820629545],
            [227.47864507273914, 316.5025060397356],
        ],
    )

    pd.testing.assert_frame_equal(result, expected)


def test_geodataframe():
    s = gpd.GeoSeries([Point(122, 55), Point(100, 1)], crs=4326)
    df = gpd.GeoSeries([Point(122, 55), Point(100, 1)], crs=4326).to_frame("geometry")

    assert isinstance(df, gpd.GeoDataFrame)
    result = s.geoazimuth_matrix(df)

    assert_frame_equal(
        result,
        pd.DataFrame([[0, 206.55650236566814], [14.860926018312751, 0]]),
        atol=1e-6,
    )


def test_none():
    s = gpd.GeoSeries([Point(116.4, 39.9), Point(121.5, 31.2)], crs=4326)

    result = s.geoazimuth_matrix()
    expected = pd.DataFrame([[0, 152.9778730470678], [335.9529431611832, 0]])

    assert_frame_equal(result, expected, atol=1e-6)
