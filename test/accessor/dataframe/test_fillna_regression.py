import pytest
import pandas as pd
from sklearn import linear_model

from dtoolkit.accessor.dataframe import fillna_regression  # noqa


@pytest.mark.parametrize(
    "df, method, X, y, how, args, kwargs, expected",
    [
        (
            pd.DataFrame(
                [
                    [1, 1, 6],
                    [1, 2, 8],
                    [2, 2, 9],
                    [2, 3, 11],
                    [3, 5, None],
                ],
                columns=["x1", "x2", "y"],
            ),
            linear_model.LinearRegression,
            ["x1", "x2"],
            "y",
            "na",
            (),
            {},
            pd.DataFrame(
                [
                    [1, 1, 6],
                    [1, 2, 8],
                    [2, 2, 9],
                    [2, 3, 11],
                    [3, 5, 16],
                ],
                columns=["x1", "x2", "y"],
            ),
        ),
        (
            pd.DataFrame(
                [
                    [1, 1, 6],
                    [1, 2, 8],
                    [2, 2, 9],
                    [2, 3, 11],
                    [3, 5, None],
                ],
                columns=["x1", "x2", "y"],
            ),
            linear_model.LinearRegression,
            ["x1", "x2"],
            "y",
            "all",
            (),
            {},
            pd.DataFrame(
                [
                    [1, 1, 6],
                    [1, 2, 8],
                    [2, 2, 9],
                    [2, 3, 11],
                    [3, 5, 16],
                ],
                columns=["x1", "x2", "y"],
            ),
        ),
        (
            pd.DataFrame(
                [
                    [1, 1, 6],
                    [1, 2, 8],
                    [2, 2, 9],
                    [2, 3, 11],
                    [3, 5, None],
                ],
                columns=["x1", "x2", "y"],
            ),
            linear_model.LinearRegression,
            "x1",
            "y",
            "na",
            (),
            {},
            pd.DataFrame(
                [
                    [1, 1, 6],
                    [1, 2, 8],
                    [2, 2, 9],
                    [2, 3, 11],
                    [3, 5, 13],
                ],
                columns=["x1", "x2", "y"],
            ),
        ),
        (
            pd.DataFrame(
                [
                    [1, 1, 6],
                    [1, 2, 8],
                    [2, 2, 9],
                    [2, 3, 11],
                    [3, 5, None],
                ],
                columns=["x1", "x2", "y"],
            ),
            linear_model.LinearRegression,
            ["x1"],
            "y",
            "all",
            (),
            {},
            pd.DataFrame(
                [
                    [1, 1, 7],
                    [1, 2, 7],
                    [2, 2, 10],
                    [2, 3, 10],
                    [3, 5, 13],
                ],
                columns=["x1", "x2", "y"],
            ),
        ),
    ],
)
def test_work(df, method, X, y, how, args, kwargs, expected):
    result = df.fillna_regression(method, X, y, how=how, *args, **kwargs)

    assert result.equals(result)


def test_error():
    df = pd.DataFrame(
        [
            [1, 1, 6],
            [1, 2, 8],
            [2, 2, 9],
            [2, 3, 11],
            [3, 5, None],
        ],
        columns=["x1", "x2", "y"],
    )
    with pytest.raises(ValueError):
        df.fillna_regression(linear_model.MultiTaskElasticNet, "x1", "y", how="blah")
