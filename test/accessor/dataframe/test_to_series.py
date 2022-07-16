import geopandas as gpd
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from pandas.testing import assert_series_equal

from dtoolkit.accessor.dataframe import to_series  # noqa: F401


@pytest.mark.parametrize(
    "df, name, index_column, value_column, expected",
    [
        (
            pd.DataFrame({"a": [1, 2]}),
            None,
            None,
            None,
            pd.Series([1, 2], name="a"),
        ),
        # dataframe -> dataframe
        (
            pd.DataFrame({"a": [1, 2], "b": [3, 4]}),
            None,
            None,
            None,
            pd.DataFrame({"a": [1, 2], "b": [3, 4]}),
        ),
        # name is not None
        (
            pd.DataFrame({"a": [1, 2]}),
            "b",
            None,
            None,
            pd.Series([1, 2], name="b"),
        ),
        # the columns of df are default
        (
            pd.DataFrame([1, 2]),
            None,
            None,
            None,
            pd.Series([1, 2], name=0),
        ),
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
        # two or more columnds dataframe -> series
        (
            pd.DataFrame({"a": [1, 2], "b": [3, 4]}),
            None,
            "b",
            "a",
            pd.Series(
                [1, 2],
                name="a",
                index=pd.Index([3, 4], name="b"),
            ),
        ),
        # two or more columnds dataframe -> series
        (
            pd.DataFrame({"a": [1, 2], "b": [3, 4]}),
            "new name",
            "b",
            "a",
            pd.Series(
                [1, 2],
                name="new name",
                index=pd.Index([3, 4], name="b"),
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


@pytest.mark.parametrize(
    "df, name, index_column, value_column, error",
    [
        (
            pd.DataFrame({"a": [1, 2], "b": [3, 4]}),
            None,
            "a",
            "a",
            ValueError,
        ),
        (
            pd.DataFrame({"a": [1, 2], "b": [3, 4]}),
            None,
            "a",
            "c",
            KeyError,
        ),
        (
            pd.DataFrame({"a": [1, 2], "b": [3, 4]}),
            None,
            "c",
            "b",
            KeyError,
        ),
    ],
)
def test_error(df, name, index_column, value_column, error):
    with pytest.raises(error):
        df.to_series(name, index_column, value_column)
