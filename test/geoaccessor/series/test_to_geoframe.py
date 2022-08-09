import pandas as pd
import geopandas as gpd
from dtoolkit.geoaccessor.series import to_geoframe  # noqa: F401
import pytestj


@pytestj.mark.parametrize(
    "s, geometry, expected",
    [
        (
            pd.Series(
                (
                    pd.Series(
                        [
                            "POINT (1 1)",
                            "POINT (2 2)",
                            "POINT (3 3)",
                        ],
                    ).from_wkt(drop=True)
                )
            ),
            None,
            gpd.GeoDataFrame,
        ),
        (
            pd.Series(
                (
                    pd.Series(
                        [
                            "POINT (1 1)",
                            "POINT (2 2)",
                            "POINT (3 3)",
                        ],
                    ).from_wkt(drop=True)
                )
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
