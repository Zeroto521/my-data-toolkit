import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from pandas.testing import assert_series_equal

from dtoolkit.accessor.dataframe import weighted_mean


@pytest.mark.parametrize(
    "df, weights, validate, top, error",
    [
        # weights (Series) its index > df.columns
        (
            pd.DataFrame({"a": [1, 2], "b": [3, 4]}),
            pd.Series({"a": 1, "b": 2, "c": 3}),
            False,
            1,
            KeyError,
        ),
        # weights (dict) its .keys() > df.columns
        (
            pd.DataFrame({"a": [1, 2], "b": [3, 4]}),
            {"a": 1, "b": 2, "c": 3},
            False,
            1,
            KeyError,
        ),
        # weights (int)
        (
            pd.DataFrame({"a": [1, 2], "b": [3, 4]}),
            1,
            False,
            1,
            TypeError,
        ),
        # weights (string)
        (
            pd.DataFrame({"a": [1, 2], "b": [3, 4]}),
            "string",
            False,
            1,
            TypeError,
        ),
        # weights (dict) its values of sub-element are string
        (
            pd.DataFrame({"a": [1, 2], "b": [3, 4]}),
            {"ab": {"a": "string"}},
            False,
            1,
            TypeError,
        ),
        # weights (dict) its values are string
        (
            pd.DataFrame({"a": [1, 2], "b": [3, 4]}),
            {"a": "string"},
            False,
            1,
            TypeError,
        ),
        # sum(weights) != top
        (
            pd.DataFrame({"a": [1, 2], "b": [3, 4]}),
            {"a": 1, "b": 2},
            True,
            4,
            ValueError,
        ),
        # weights (list) its length != df.columns
        (
            pd.DataFrame({"a": [1, 2], "b": [3, 4]}),
            [1],
            False,
            1,
            ValueError,
        ),
    ],
)
def test_error(df, weights, validate, top, error):
    with pytest.raises(error):
        weighted_mean(df, weights, validate=validate, top=top)


@pytest.mark.parametrize(
    "df, weights, validate, top, drop, expected",
    [
        # test Series
        (
            pd.DataFrame({"a": [1, 2], "b": [2, 4]}),
            pd.Series({"a": 0.5, "b": 0.5}),
            False,
            1,
            False,
            pd.Series([1.5, 3]),
        ),
        # test Series
        (
            pd.DataFrame({"a": [1, 2], "b": [2, 4]}),
            pd.Series({"a": 0.5, "b": 0.5}),
            False,
            1,
            True,
            pd.Series([1.5, 3]),
        ),
        # test Series
        (
            pd.DataFrame({"a": [1, 2], "b": [2, 4]}),
            pd.Series({"a": 0.5, "b": 0.5}, name="ab"),
            False,
            1,
            True,
            pd.Series([1.5, 3], name="ab"),
        ),
        # test Series
        (
            pd.DataFrame({"a": [1, 2], "b": [2, 4]}),
            pd.Series({"a": 0.5, "b": 0.5}, name="ab"),
            False,
            1,
            False,
            pd.DataFrame({"a": [1, 2], "ab": [1.5, 3], "b": [2, 4]}),
        ),
        # test validate and top
        (
            pd.DataFrame({"a": [1, 2], "b": [2, 4]}),
            pd.Series({"a": 0.5, "b": 0.5}),
            True,
            1,
            False,
            pd.Series([1.5, 3]),
        ),
        # test validate and top
        (
            pd.DataFrame({"a": [1, 2], "b": [2, 4]}),
            pd.Series({"a": 2, "b": 1}),
            True,
            3,
            False,
            pd.Series([4 / 3, 8 / 3]),
        ),
        # test dict
        (
            pd.DataFrame({"a": [1, 2], "b": [2, 4]}),
            {"a": 0.5, "b": 0.5},
            False,
            3,
            False,
            pd.Series([1.5, 3]),
        ),
        # test dict
        (
            pd.DataFrame({"a": [1, 2], "b": [2, 4]}),
            {"ab": {"a": 0.5, "b": 0.5}, "ab-a": {"ab": 1, "a": 1}},
            False,
            3,
            False,
            pd.DataFrame(
                {
                    "a": [1, 2],
                    "ab": [1.5, 3],
                    "ab-a": [1.25, 2.5],
                    "b": [2, 4],
                },
                index=pd.Index([0, 1], dtype='object'),
            ),
        ),
    ],
)
def test_work(df, weights, validate, top, drop, expected):
    result = df.weighted_mean(weights, validate=validate, top=top, drop=drop)

    assert_equal = assert_series_equal
    if isinstance(expected, pd.DataFrame):
        assert_equal = assert_frame_equal

    assert_equal(result, expected)
