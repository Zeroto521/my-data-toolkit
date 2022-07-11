import pandas as pd
import geopandas as gpd
import pytest
from pandas.testing import assert_series_equal
from geopandas.testing import assert_geoseries_equal

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
                ).from_wkt(drop=True)
            ),
            None,
            pd.Series(
                [
                    "POINT (1 1)",
                    "POINT (2 2)",
                    "POINT (3 3)",
                ],
            ).from_wkt(drop=True),
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
                ).from_wkt(drop=True)
            ),
            3857,
            pd.Series(
                [
                    "POINT (1 1)",
                    "POINT (2 2)",
                    "POINT (3 3)",
                ],
            ).from_wkt(drop=True, crs=3857),
        ),
        (
            pd.Series(
                pd.Series(
                    [
                        "POINT (1 1)",
                        "POINT (2 2)",
                        "POINT (3 3)",
                    ],
                ).from_wkt(drop=True, crs=3857)
            ),
            4326,
            (
                pd.Series(
                    [
                        "POINT (1 1)",
                        "POINT (2 2)",
                        "POINT (3 3)",
                    ],
                )
                .from_wkt(drop=True, crs=3857)
                .to_crs(4326)
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
