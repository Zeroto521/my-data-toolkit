import pandas as pd
import pytest
from geopandas.testing import assert_geoseries_equal
from pandas.testing import assert_series_equal

from dtoolkit.geoaccessor.series import to_geoseries  # noqa: F401


@pytest.mark.parametrize(
    "s, crs, expected",
    [
        # test series -> series
        (
            pd.Series(
                [
                    "POINT (1 1)",
                    "POINT (2 2)",
                    "POINT (3 3)",
                ],
            ),
            None,
            pd.Series(
                [
                    "POINT (1 1)",
                    "POINT (2 2)",
                    "POINT (3 3)",
                ],
            ),
        ),
        # test series -> geoseries
        (
            pd.Series(
                pd.Series(
                    [
                        "POINT (1 1)",
                        "POINT (2 2)",
                        "POINT (3 3)",
                    ],
                    name="wkt",
                )
                .from_wkt()
                .geometry,
            ),
            None,
            pd.Series(
                [
                    "POINT (1 1)",
                    "POINT (2 2)",
                    "POINT (3 3)",
                ],
                name="wkt",
            )
            .from_wkt()
            .geometry,
        ),
        # test crs
        (
            pd.Series(
                pd.Series(
                    [
                        "POINT (1 1)",
                        "POINT (2 2)",
                        "POINT (3 3)",
                    ],
                    name="wkt",
                )
                .from_wkt()
                .geometry,
            ),
            4326,
            pd.Series(
                [
                    "POINT (1 1)",
                    "POINT (2 2)",
                    "POINT (3 3)",
                ],
                name="wkt",
            )
            .from_wkt(crs=4326)
            .geometry,
        ),
        (
            pd.Series(
                pd.Series(
                    [
                        "POINT (1 1)",
                        "POINT (2 2)",
                        "POINT (3 3)",
                    ],
                    name="wkt",
                )
                .from_wkt(crs=4326)
                .geometry,
            ),
            4326,
            (
                pd.Series(
                    [
                        "POINT (1 1)",
                        "POINT (2 2)",
                        "POINT (3 3)",
                    ],
                    name="wkt",
                )
                .from_wkt(crs=4326)
                .geometry
            ),
        ),
    ],
)
def test_work(s, crs, expected):
    assert isinstance(s, pd.Series)
    result = s.to_geoseries(crs=crs)

    if isinstance(expected, pd.Series):
        assert_series_equal(result, expected)
    else:
        assert_geoseries_equal(result, expected)
