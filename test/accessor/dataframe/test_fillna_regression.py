import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from sklearn import linear_model
from sklearn import tree

from dtoolkit.accessor.dataframe import fillna_regression  # noqa


@pytest.mark.parametrize(
    "df, method, columns, how, kwargs, expected",
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
            {"y": ["x1", "x2"]},
            "na",
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
            linear_model.Ridge,
            {"y": ["x1", "x2"]},
            "na",
            {},
            pd.DataFrame(
                [
                    [1, 1, 6],
                    [1, 2, 8],
                    [2, 2, 9],
                    [2, 3, 11],
                    [3, 5, 13.9],
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
            {"y": ["x1", "x2"]},
            "all",
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
            {"y": "x1"},
            "na",
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
            {"y": "x2"},
            "na",
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
            {"y": ["x1"]},
            "all",
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
            {"y": pd.Index(["x1"])},
            "all",
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
        (
            pd.DataFrame(
                [
                    [1, 1, None],
                    [1, 2, 8],
                    [2, 2, 9],
                    [2, 3, 11],
                    [3, 5, None],
                ],
                columns=["x1", "x2", "y"],
            ),
            tree.DecisionTreeRegressor,
            {"y": ["x1", "x2"]},
            "na",
            dict(criterion="friedman_mse", splitter="best"),
            pd.DataFrame(
                [
                    [1, 1, 8],
                    [1, 2, 8],
                    [2, 2, 9],
                    [2, 3, 11],
                    [3, 5, 11],
                ],
                columns=["x1", "x2", "y"],
            ),
        ),
        (
            pd.DataFrame(
                [
                    [1, 1, None],
                    [1, 2, 8],
                    [2, 2, 9],
                    [2, 3, 11],
                    [3, 5, None],
                ],
                columns=["x1", "x2", "y"],
            ),
            tree.DecisionTreeRegressor,
            {"y": ["x1", "x2"]},
            "na",
            {},
            pd.DataFrame(
                [
                    [1, 1, 8],
                    [1, 2, 8],
                    [2, 2, 9],
                    [2, 3, 11],
                    [3, 5, 11],
                ],
                columns=["x1", "x2", "y"],
            ),
        ),
        (
            pd.DataFrame(
                [
                    [1, 1, None, 6],
                    [1, 2, 8, 8],
                    [2, 2, 9, 9],
                    [2, 3, 11, 11],
                    [3, 5, None, None],
                ],
                columns=["x1", "x2", "y1", "y2"],
            ),
            tree.DecisionTreeRegressor,
            {"y2": ["x1"], "y1": ["x1", "x2"]},
            "na",
            {},
            pd.DataFrame(
                [
                    [1, 1, 8, 6],
                    [1, 2, 8, 8],
                    [2, 2, 9, 9],
                    [2, 3, 11, 11],
                    [3, 5, 11, 10],
                ],
                columns=["x1", "x2", "y1", "y2"],
            ),
        ),
    ],
)
def test_work(df, method, columns, how, kwargs, expected):
    result = df.fillna_regression(method, columns, how=how, **kwargs)

    assert_frame_equal(result, expected, check_dtype=False)


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
        df.fillna_regression(linear_model.MultiTaskElasticNet, {"y": "x1"}, how="blah")
