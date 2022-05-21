import numpy as np
import pandas as pd
import pytest

from dtoolkit.accessor.series import error_report  # noqa


@pytest.mark.parametrize(
    "true, predicted, columns, expected",
    [
        # both Series
        (
            pd.Series([1, 2]),
            pd.Series([2, 1]),
            None,
            pd.DataFrame(
                {
                    "true value": [1, 2],
                    "predicted value": [2, 1],
                    "absolute error": [1, 1],
                    "relative error": [1, 0.5],
                },
            ),
        ),
        # test name
        (
            pd.Series([1, 2], name="x"),
            pd.Series([2, 1], name="y"),
            None,
            pd.DataFrame(
                {
                    "x": [1, 2],
                    "y": [2, 1],
                    "absolute error": [1, 1],
                    "relative error": [1, 0.5],
                },
            ),
        ),
        # test columns
        (
            pd.Series([1, 2], name="x"),
            pd.Series([2, 1], name="y"),
            ["a", "b", "c", "d"],
            pd.DataFrame(
                {
                    "a": [1, 2],
                    "b": [2, 1],
                    "c": [1, 1],
                    "d": [1, 0.5],
                },
            ),
        ),
        # predicted is array-like type
        (
            pd.Series([1, 2]),
            [2, 1],
            None,
            pd.DataFrame(
                {
                    "true value": [1, 2],
                    "predicted value": [2, 1],
                    "absolute error": [1, 1],
                    "relative error": [1, 0.5],
                },
            ),
        ),
        # predicted is array-like type
        (
            pd.Series([1, 2]),
            np.array([2, 1], dtype="int64"),
            None,
            pd.DataFrame(
                {
                    "true value": [1, 2],
                    "predicted value": [2, 1],
                    "absolute error": [1, 1],
                    "relative error": [1, 0.5],
                },
            ),
        ),
        # true has index
        (
            pd.Series([1, 2], index=["a", "b"]),
            pd.Series([2, 1], index=["a", "b"]),
            None,
            pd.DataFrame(
                {
                    "true value": [1, 2],
                    "predicted value": [2, 1],
                    "absolute error": [1, 1],
                    "relative error": [1, 0.5],
                },
                index=["a", "b"],
            ),
        ),
        # true has index
        (
            pd.Series([1, 2], index=["a", "b"]),
            [2, 1],
            None,
            pd.DataFrame(
                {
                    "true value": [1, 2],
                    "predicted value": [2, 1],
                    "absolute error": [1, 1],
                    "relative error": [1, 0.5],
                },
                index=["a", "b"],
            ),
        ),
        # true has index
        (
            pd.Series([1, 2], index=["a", "b"]),
            np.array([2, 1], dtype="int64"),
            None,
            pd.DataFrame(
                {
                    "true value": [1, 2],
                    "predicted value": [2, 1],
                    "absolute error": [1, 1],
                    "relative error": [1, 0.5],
                },
                index=["a", "b"],
            ),
        ),
    ],
)
def test_work(true, predicted, columns, expected):
    result = true.error_report(predicted, columns=columns)

    assert result.equals(expected)


@pytest.mark.parametrize(
    "true, predicted, columns, error",
    [
        # different lengths
        (pd.Series([1, 2, 3]), pd.Series([2, 1]), None, IndexError),
        # different indexes
        (pd.Series([1, 2]), pd.Series([2, 1], index=["a", "b"]), None, IndexError),
        # test len(columns) != 4
        (pd.Series([1, 2]), pd.Series([2, 1]), [], IndexError),
        (pd.Series([1, 2]), pd.Series([2, 1]), range(5), IndexError),
    ],
)
def test_error(true, predicted, columns, error):
    with pytest.raises(error):
        true.error_report(predicted, columns=columns)
