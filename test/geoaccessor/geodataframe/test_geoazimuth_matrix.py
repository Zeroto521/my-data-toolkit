import geopandas as gpd
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from shapely import Point

from dtoolkit.geoaccessor.geodataframe import geoazimuth_matrix


def test_geodataframe_pair():
    df = gpd.GeoDataFrame(
        geometry=gpd.GeoSeries([Point(116.4, 39.9), Point(121.5, 31.2)], crs=4326),
    )
    other = gpd.GeoDataFrame(
        geometry=gpd.GeoSeries([Point(120, 30), Point(110, 40)], crs=4326),
    )

    result = df.geoazimuth_matrix(other)

    assert_frame_equal(
        result,
        pd.DataFrame(
            [
                [162.34309829667646, 273.22246820629545],
                [227.47864507273914, 316.5025060397356],
            ],
        ),
        atol=1e-6,
    )


def test_geodataframe_none():
    df = gpd.GeoDataFrame(
        geometry=gpd.GeoSeries([Point(116.4, 39.9), Point(121.5, 31.2)], crs=4326),
    )

    result = df.geoazimuth_matrix()

    assert_frame_equal(
        result,
        pd.DataFrame([[0, 152.9778730470678], [335.9529431611832, 0]]),
        atol=1e-6,
    )


def test_geodataframe_from_geoseries():
    df = gpd.GeoDataFrame(
        geometry=gpd.GeoSeries([Point(116.4, 39.9), Point(121.5, 31.2)], crs=4326),
    )
    other = gpd.GeoSeries([Point(120, 30), Point(110, 40)], crs=4326)

    result = df.geoazimuth_matrix(other)

    assert_frame_equal(
        result,
        pd.DataFrame(
            [
                [162.34309829667646, 273.22246820629545],
                [227.47864507273914, 316.5025060397356],
            ],
        ),
        atol=1e-6,
    )


@pytest.mark.parametrize(
    "df, other, error",
    [
        (
            gpd.GeoDataFrame(
                geometry=gpd.GeoSeries([Point(120, 30), Point(110, 40)], crs=4326),
            ),
            Point(1, 1),
            TypeError,
        ),
        (
            gpd.GeoDataFrame(
                geometry=gpd.GeoSeries([Point(120, 30), Point(110, 40)], crs=4326),
            ),
            "string",
            TypeError,
        ),
        (
            gpd.GeoDataFrame(
                geometry=gpd.GeoSeries([Point(120, 30), Point(110, 40)]),
            ),
            gpd.GeoSeries([Point(120, 30)], crs=4326),
            ValueError,
        ),
    ],
)
def test_error(df, other, error):
    with pytest.raises(error):
        geoazimuth_matrix(df, other=other)
