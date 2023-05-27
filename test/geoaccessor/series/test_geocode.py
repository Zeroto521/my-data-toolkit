import geopandas as gpd
import pandas as pd
import pytest
from geopandas.testing import assert_geodataframe_equal

from dtoolkit.geoaccessor.series import geocode


pytest.importorskip("geopy")


@pytest.mark.parametrize(
    "s, drop, error",
    [
        (
            pd.Series(
                [
                    "boston, ma",
                    "1600 pennsylvania ave. washington, dc",
                ],
            ),
            False,
            ValueError,
        ),
    ],
)
def test_error(s, drop, error):
    with pytest.raises(error):
        geocode(s, drop=drop)


def test_type():
    s = pd.Series(
        [
            "boston, ma",
            "1600 pennsylvania ave. washington, dc",
        ],
        name="address",
    )

    result = s.geocode()

    assert isinstance(result, gpd.GeoDataFrame)


def test_work():
    s = pd.Series([".", "South Pole"], name="address").geocode()
    expected = gpd.GeoDataFrame(
        {
            "address": [".", "South Pole"],
            "geometry": gpd.GeoSeries.from_wkt(
                [None, "POINT (0 -90)"],
                crs=4326,
            ),
        },
    )

    assert_geodataframe_equal(result, expected)


def test_geolocator():
    from geopy.geocoders import get_geocoder_for_service

    result = pd.Series(["South Pole"], name="address").geocode(
        provider=get_geocoder_for_service("photon")
    )
    expected = gpd.GeoDataFrame(
        {
            "address": ["South Pole"],
            "geometry": gpd.GeoSeries.from_wkt(["POINT (0 -90)"], crs=4326),
        },
    )

    assert_geodataframe_equal(result, expected)
