import geopandas as gpd
import pandas as pd
import pytest
from shapely.geometry import Point

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


def test_index():
    geometry = gpd.GeoSeries([Point(1, 1), Point(2, 2)], index=[1, 2])
    s = pd.Series([1, 2], "h3")
    df = s.to_geoframe(geometry=geometry)

    assert df.geometry.notnull().all()
