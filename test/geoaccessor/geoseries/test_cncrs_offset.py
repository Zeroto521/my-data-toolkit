import geopandas as gpd
import pytest
from geopandas.testing import assert_geoseries_equal

from dtoolkit.geoaccessor.geoseries import cncrs_offset


@pytest.mark.parametrize(
    "s, from_crs, to_crs, error",
    [
        (gpd.GeoSeries.from_wkt(["POINT (0 0)"]), "", "", ValueError),
        (gpd.GeoSeries.from_wkt(["POINT (0 0)"], crs=4326), "", "", ValueError),
        (
            gpd.GeoSeries.from_wkt(["POINT (0 0)"], crs=4326),
            "error-CRS",
            "",
            ValueError,
        ),
        (
            gpd.GeoSeries.from_wkt(["POINT (0 0)"], crs=4326),
            "wgs84",
            "error-CRS",
            ValueError,
        ),
        (
            gpd.GeoSeries.from_wkt(["POINT (0 0)"], crs=4326),
            "WGS84",
            "wgs84",
            ValueError,
        ),
    ],
)
def test_error(s, from_crs, to_crs, error):
    with pytest.raises(error):
        cncrs_offset(s, from_crs, to_crs)


@pytest.mark.parametrize(
    "s, from_crs, to_crs, expected",
    [
        # out of China
        (
            gpd.GeoSeries.from_wkt(["POINT (0 0)"], crs=4326),
            "wgs84",
            "gcj02",
            gpd.GeoSeries.from_wkt(["POINT (0 0)"], crs=4326),
        ),
        # wgs84 to gcj02
        (
            gpd.GeoSeries.from_wkt(["POINT (0 0)", "POINT (128.543 37.065)"], crs=4326),
            "wgs84",
            "gcj02",
            gpd.GeoSeries.from_wkt(
                [
                    "POINT (0 0)",
                    "POINT (128.54820547949757 37.065651049489816)",
                ],
                crs=4326,
            ),
        ),
        # wgs84 to bd09
        (
            gpd.GeoSeries.from_wkt(["POINT (0 0)", "POINT (128.543 37.065)"], crs=4326),
            "wgs84",
            "bd09",
            gpd.GeoSeries.from_wkt(
                [
                    "POINT (0 0)",
                    "POINT (128.55468192918485 37.07168344938498)",
                ],
                crs=4326,
            ),
        ),
        # gcj02 to wgs84
        (
            gpd.GeoSeries.from_wkt(["POINT (0 0)", "POINT (128.543 37.065)"], crs=4326),
            "gcj02",
            "wgs84",
            gpd.GeoSeries.from_wkt(
                [
                    "POINT (0 0)",
                    "POINT (128.53779452050244 37.06434895051018)",
                ],
                crs=4326,
            ),
        ),
        # gcj02 to bd09
        (
            gpd.GeoSeries.from_wkt(["POINT (0 0)", "POINT (128.543 37.065)"], crs=4326),
            "gcj02",
            "bd09",
            gpd.GeoSeries.from_wkt(
                [
                    "POINT (0 0)",
                    "POINT (128.54944656269413 37.07113427883019)",
                ],
                crs=4326,
            ),
        ),
        # bd09 to wgs84
        (
            gpd.GeoSeries.from_wkt(["POINT (0 0)", "POINT (128.543 37.065)"], crs=4326),
            "bd09",
            "wgs84",
            gpd.GeoSeries.from_wkt(
                [
                    "POINT (0 0)",
                    "POINT (128.53136876750008 37.0580926428705)",
                ],
                crs=4326,
            ),
        ),
        # bd09 to gcj02
        (
            gpd.GeoSeries.from_wkt(["POINT (0 0)", "POINT (128.543 37.065)"], crs=4326),
            "bd09",
            "gcj02",
            gpd.GeoSeries.from_wkt(
                [
                    "POINT (0 0)",
                    "POINT (128.5365893261212 37.058754503281534)",
                ],
                crs=4326,
            ),
        ),
    ],
)
def test_work(s, from_crs, to_crs, expected):
    result = s.cncrs_offset(from_crs, to_crs)

    assert_geoseries_equal(result, expected, check_less_precise=True)


def test_avoid_mutating_original_data():
    s = gpd.GeoSeries.from_wkt(["POINT (0 0)", "POINT (120 30)"], crs=4326)
    s_copy = s.copy()

    result = s.cncrs_offset("wgs84", "gcj02")

    assert_geoseries_equal(s, s_copy)

    with pytest.raises(AssertionError):
        assert_geoseries_equal(s, result)
