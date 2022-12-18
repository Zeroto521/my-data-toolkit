import geopandas as gpd
import pandas as pd
from pandas.testing import assert_series_equal

import pytest

from dtoolkit.geoaccessor.geodataframe import get_coordinates


@pytest.mark.parametrize(
    "s, expected",
    [
        (
            gpd.GeoSeries.from_wkt(["POINT (0 0)"]).to_frame("geometry"),
            pd.Series([[[0.0, 0.0]]], name="geometry"),
        ),
        (
            gpd.GeoSeries.from_wkt(["LINESTRING (2 2, 4 4)"]).to_frame("geometry"),
            pd.Series([[[2.0, 2.0], [4.0, 4.0]]], name="geometry"),
        ),
        (
            gpd.GeoSeries.from_wkt([None]).to_frame("geometry"),
            pd.Series([[]], name="geometry"),
        ),
    ],
)
def test_work(s, expected):
    result = get_coordinates(s)

    assert_series_equal(result, expected)
