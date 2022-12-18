import geopandas as gpd
import pandas as pd
from pandas.testing import assert_series_equal

from dtoolkit.geoaccessor.geodataframe import coordinates  # noqa: F401


def test_work():
    result = (
        gpd.GeoSeries.from_wkt(
            [
                "POINT (0 0)",
                "LINESTRING (2 2, 4 4)",
                None,
            ],
        )
        .to_frame("geometry")
        .coordinates()
    )

    expected = pd.Series(
        [
            [[0.0, 0.0]],
            [[2.0, 2.0], [4.0, 4.0]],
            [],
        ],
        name="geometry",
    )

    assert_series_equal(result, expected)
