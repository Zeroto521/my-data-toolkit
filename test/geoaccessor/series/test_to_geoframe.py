import geopandas as gpd
import pandas as pd
import pytest
from shapely.geometry import Point

from geopandas.testing import assert_geodataframe_equal

from dtoolkit.geoaccessor.series import to_geoframe  # noqa: F401


@pytest.mark.parametrize(
    "s, geometry, expected",
    [
        (
            pd.Series(
                pd.Series(
                    [
                        "POINT (1 1)",
                        "POINT (2 2)",
                        "POINT (3 3)",
                    ],
                ).from_wkt(drop=True),
            ),
            None,
            gpd.GeoDataFrame,
        ),
        (
            pd.Series(
                pd.Series(
                    [
                        "POINT (1 1)",
                        "POINT (2 2)",
                        "POINT (3 3)",
                    ],
                ).from_wkt(drop=True),
            ),
            (
                pd.Series(
                    [
                        "POINT (1 1)",
                        "POINT (2 2)",
                        "POINT (3 3)",
                    ],
                ).from_wkt(drop=True)
            ),
            gpd.GeoDataFrame,
        ),
        (
            pd.Series(
                [
                    "POINT (1 1)",
                    "POINT (2 2)",
                    "POINT (3 3)",
                ],
            ),
            (
                pd.Series(
                    [
                        "POINT (1 1)",
                        "POINT (2 2)",
                        "POINT (3 3)",
                    ],
                ).from_wkt(drop=True)
            ),
            gpd.GeoDataFrame,
        ),
        (
            pd.Series(
                [
                    "POINT (1 1)",
                    "POINT (2 2)",
                    "POINT (3 3)",
                ],
            ),
            None,
            pd.DataFrame,
        ),
    ],
)
def test_type(s, geometry, expected):
    result = s.to_geoframe(geometry=geometry)

    assert isinstance(s, pd.Series)
    assert isinstance(result, expected)


@pytest.mark.parametrize(
    "s, geometry, expected",
    [
        # s's index different from geometry's index
        (
            pd.Series([1, 2], name="name"),
            gpd.GeoSeries([Point(1, 1), Point(2, 2)], index=[1, 2]),
            gpd.GeoDataFrame(
                {
                    "name": [1, 2],
                    "geometry": [None, Point(1, 1)],
                },
            ),
        ),
    ],
)
def test_index():
    result = to_geoframe(s, geometry=geometry)

    assert_geodataframe_equal(result, expected)
