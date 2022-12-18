"""
This is a test for `dtoolkit.accessor.dataframe.to_series`,
while the input is `GeoDataFrame`.
"""
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from pandas.testing import assert_series_equal

from dtoolkit.accessor.dataframe import to_series  # noqa: F401


gpd = pytest.importorskip("geopandas")


@pytest.mark.parametrize(
    "df, name, index_column, value_column, expected",
    [
        # geodataframe -> geodataframe
        (
            gpd.GeoDataFrame({"a": [1, 2], "b": [3, 4]}),
            None,
            None,
            None,
            gpd.GeoDataFrame({"a": [1, 2], "b": [3, 4]}),
        ),
        # geodataframe -> geodataframe
        (
            gpd.GeoDataFrame.from_features(
                {
                    "type": "FeatureCollection",
                    "features": [
                        {
                            "type": "Feature",
                            "properties": {"col1": "name1"},
                            "geometry": {
                                "type": "Point",
                                "coordinates": (1.0, 2.0),
                            },
                        },
                        {
                            "type": "Feature",
                            "properties": {"col1": "name2"},
                            "geometry": {
                                "type": "Point",
                                "coordinates": (2.0, 1.0),
                            },
                        },
                    ],
                },
            ),
            None,
            None,
            None,
            gpd.GeoDataFrame.from_features(
                {
                    "type": "FeatureCollection",
                    "features": [
                        {
                            "type": "Feature",
                            "properties": {"col1": "name1"},
                            "geometry": {
                                "type": "Point",
                                "coordinates": (1.0, 2.0),
                            },
                        },
                        {
                            "type": "Feature",
                            "properties": {"col1": "name2"},
                            "geometry": {
                                "type": "Point",
                                "coordinates": (2.0, 1.0),
                            },
                        },
                    ],
                },
            ),
        ),
        # geodataframe -> geoseries
        (
            gpd.GeoDataFrame({"a": [1, 2]}),
            None,
            None,
            None,
            pd.Series([1, 2], name="a"),
        ),
        # geodataframe -> geoseries
        (
            gpd.GeoDataFrame.from_features(
                {
                    "type": "FeatureCollection",
                    "features": [
                        {
                            "type": "Feature",
                            "properties": {},
                            "geometry": {
                                "type": "Point",
                                "coordinates": (1.0, 2.0),
                            },
                        },
                        {
                            "type": "Feature",
                            "properties": {},
                            "geometry": {
                                "type": "Point",
                                "coordinates": (2.0, 1.0),
                            },
                        },
                    ],
                },
            ),
            None,
            None,
            None,
            gpd.GeoSeries.from_wkt(
                [
                    "POINT (1 2)",
                    "POINT (2 1)",
                ],
                name="geometry",
            ),
        ),
    ],
)
def test_work(df, name, index_column, value_column, expected):
    result = df.to_series(name, index_column, value_column)

    if isinstance(expected, pd.Series):
        assert_series_equal(result, expected)
    else:
        assert_frame_equal(result, expected)
