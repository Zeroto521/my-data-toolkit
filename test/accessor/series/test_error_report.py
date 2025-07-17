import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from dtoolkit.accessor.series import error_report  # noqa: F401


@pytest.mark.parametrize(
    "true, predicted, absolute_error, relative_error, expected",
    [
        # both Series
        (
            pd.Series([1, 2]),
            pd.Series([2, 1]),
            None,
            None,
            pd.DataFrame(
                {
                    "true": [1, 2],
                    "predicted": [2, 1],
                    "absolute_error": [1, 1],
                    "relative_error": [1, 0.5],
                },
            ),
        ),
        # test name
        (
            pd.Series([1, 2], name="x"),
            pd.Series([2, 1], name="y"),
            None,
            None,
            pd.DataFrame(
                {
                    "x": [1, 2],
                    "y": [2, 1],
                    "absolute_error": [1, 1],
                    "relative_error": [1, 0.5],
                },
            ),
        ),
        # test columns
        (
            pd.Series([1, 2], name="x"),
            pd.Series([2, 1], name="y"),
            "c",
            "d",
            pd.DataFrame(
                {
                    "x": [1, 2],
                    "y": [2, 1],
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
            None,
            pd.DataFrame(
                {
                    "true": [1, 2],
                    "predicted": [2, 1],
                    "absolute_error": [1, 1],
                    "relative_error": [1, 0.5],
                },
            ),
        ),
        # predicted is array-like type
        (
            pd.Series([1, 2]),
            np.array([2, 1], dtype="int64"),
            None,
            None,
            pd.DataFrame(
                {
                    "true": [1, 2],
                    "predicted": [2, 1],
                    "absolute_error": [1, 1],
                    "relative_error": [1, 0.5],
                },
            ),
        ),
        # true has index
        (
            pd.Series([1, 2], index=["a", "b"]),
            pd.Series([2, 1], index=["a", "b"]),
            None,
            None,
            pd.DataFrame(
                {
                    "true": [1, 2],
                    "predicted": [2, 1],
                    "absolute_error": [1, 1],
                    "relative_error": [1, 0.5],
                },
                index=["a", "b"],
            ),
        ),
        # true has index
        (
            pd.Series([1, 2], index=["a", "b"]),
            [2, 1],
            None,
            None,
            pd.DataFrame(
                {
                    "true": [1, 2],
                    "predicted": [2, 1],
                    "absolute_error": [1, 1],
                    "relative_error": [1, 0.5],
                },
                index=["a", "b"],
            ),
        ),
        # true has index
        (
            pd.Series([1, 2], index=["a", "b"]),
            np.array([2, 1], dtype="int64"),
            None,
            None,
            pd.DataFrame(
                {
                    "true": [1, 2],
                    "predicted": [2, 1],
                    "absolute_error": [1, 1],
                    "relative_error": [1, 0.5],
                },
                index=["a", "b"],
            ),
        ),
    ],
)
def test_work(true, predicted, absolute_error, relative_error, expected):
    result = true.error_report(
        predicted,
        absolute_error=absolute_error or "absolute_error",
        relative_error=relative_error or "relative_error",
    )

    assert_frame_equal(result, expected)


@pytest.mark.parametrize(
    "true, predicted, error",
    [
        # different lengths
        (pd.Series([1, 2, 3]), pd.Series([2, 1]), IndexError),
        # different indexes
        (pd.Series([1, 2]), pd.Series([2, 1], index=["a", "b"]), IndexError),
    ],
)
def test_error(true, predicted, error):
    with pytest.raises(error):
        true.error_report(predicted)
