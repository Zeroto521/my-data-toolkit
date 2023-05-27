import geopandas as gpd
import pandas as pd
import pytest
from geopandas import assert_geodataframe_equal

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
    s = pd.Series([None, "South Pole"], name="address")
    expected = gpd.GeoDataFrame(
        {
            "address": [None, "South Pole"],
            "geometry": gpd.GeoSeries.from_wkt(
                ["POINT (-90 0)", "POINT (-180 -90)"],
                crs=4326,
            ),
        },
    )

    assert_geodataframe_equal(s.geocode(), expected)
