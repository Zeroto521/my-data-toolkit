import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from dtoolkit.accessor.dataframe import decompose  # noqa: F401


decomposition = pytest.importorskip("sklearn.decomposition")


@pytest.mark.parametrize(
    "df, method, columns, drop, kwargs, expected",
    [
        (
            pd.DataFrame(
                [
                    [1, 1, 1],
                    [0, 1, 1],
                    [1, 1, 1],
                    [0, 1, 1],
                ],
                columns=["a", "b", "c"],
            ),
            decomposition.PCA,
            None,
            False,
            {},
            pd.DataFrame(
                [
                    [0.5, 0, 0],
                    [-0.5, 0, 0],
                    [0.5, 0, 0],
                    [-0.5, 0, 0],
                ],
                columns=["a", "b", "c"],
            ),
        ),
        (
            pd.DataFrame(
                [
                    [1, 1, 1],
                    [0, 1, 1],
                    [1, 1, 1],
                    [0, 1, 1],
                ],
                columns=["a", "b", "c"],
            ),
            decomposition.PCA,
            None,
            True,
            {},
            pd.DataFrame(
                [
                    [0.5, 0, 0],
                    [-0.5, 0, 0],
                    [0.5, 0, 0],
                    [-0.5, 0, 0],
                ],
                columns=["a", "b", "c"],
            ),
        ),
        (
            pd.DataFrame(
                [
                    [1, 1, 1],
                    [0, 1, 1],
                    [1, 1, 1],
                    [0, 1, 1],
                ],
                columns=["a", "b", "c"],
            ),
            decomposition.PCA,
            ["a", "b"],
            False,
            {},
            pd.DataFrame(
                [
                    [0.5, 0, 1],
                    [-0.5, 0, 1],
                    [0.5, 0, 1],
                    [-0.5, 0, 1],
                ],
                columns=["a", "b", "c"],
            ),
        ),
        (
            pd.DataFrame(
                [
                    [1, 1, 1],
                    [0, 1, 1],
                    [1, 1, 1],
                    [0, 1, 1],
                ],
                columns=["a", "b", "c"],
            ),
            decomposition.PCA,
            pd.Index(["a", "b"]),
            False,
            {},
            pd.DataFrame(
                [
                    [0.5, 0, 1],
                    [-0.5, 0, 1],
                    [0.5, 0, 1],
                    [-0.5, 0, 1],
                ],
                columns=["a", "b", "c"],
            ),
        ),
        (
            pd.DataFrame(
                [
                    [1, 1, 1],
                    [0, 1, 1],
                    [1, 1, 1],
                    [0, 1, 1],
                ],
                columns=["a", "b", "c"],
            ),
            decomposition.PCA,
            {"A": ["a", "b"]},
            False,
            {},
            pd.DataFrame(
                [
                    [0.5, 1, 1, 1],
                    [-0.5, 0, 1, 1],
                    [0.5, 1, 1, 1],
                    [-0.5, 0, 1, 1],
                ],
                columns=["A", "a", "b", "c"],
            ),
        ),
        (
            pd.DataFrame(
                [
                    [1, 1, 1],
                    [0, 1, 1],
                    [1, 1, 1],
                    [0, 1, 1],
                ],
                columns=["a", "b", "c"],
            ),
            decomposition.PCA,
            {"A": ["a", "b"]},
            True,
            {},
            pd.DataFrame(
                [
                    [0.5, 1],
                    [-0.5, 1],
                    [0.5, 1],
                    [-0.5, 1],
                ],
                columns=["A", "c"],
            ),
        ),
        (
            pd.DataFrame(
                [
                    [1, 1, 1],
                    [0, 1, 1],
                    [1, 1, 1],
                    [0, 1, 1],
                ],
                columns=["a", "b", "c"],
            ),
            decomposition.PCA,
            {"X": ["a", "b"], ("A", "B"): ["a", "c"], "C": "c", "a": "a"},
            False,
            {},
            pd.DataFrame(
                [
                    [0.5, 0.0, 0.0, 0.5, 0.5, 1.0, 1.0],
                    [-0.5, 0.0, 0.0, -0.5, -0.5, 1.0, 1.0],
                    [0.5, 0.0, 0.0, 0.5, 0.5, 1.0, 1.0],
                    [-0.5, -0.0, 0.0, -0.5, -0.5, 1.0, 1.0],
                ],
                columns=["A", "B", "C", "X", "a", "b", "c"],
            ),
        ),
        (
            pd.DataFrame(
                [
                    [1, 1, 1],
                    [0, 1, 1],
                    [1, 1, 1],
                    [0, 1, 1],
                ],
                columns=["a", "b", "c"],
            ),
            decomposition.PCA,
            {"X": ["a", "b"], ("A", "B"): ["a", "c"], "C": "c", "a": "a"},
            True,
            {},
            pd.DataFrame(
                [
                    [0.5, 0.5, 0.0, 0.0, 0.5],
                    [-0.5, -0.5, 0.0, 0.0, -0.5],
                    [0.5, 0.5, 0.0, 0.0, 0.5],
                    [-0.5, -0.5, -0.0, 0.0, -0.5],
                ],
                columns=["X", "A", "B", "C", "a"],
            ),
        ),
    ],
)
def test_work(df, method, columns, drop, kwargs, expected):
    result = df.decompose(method, columns, drop=drop, **kwargs)

    assert_frame_equal(result, expected, check_dtype=False)


@pytest.mark.parametrize(
    "df, method, columns, drop, kwargs, error",
    [
        (
            pd.DataFrame(
                [
                    [1, 1, 1],
                    [0, 1, 1],
                    [1, 1, 1],
                    [0, 1, 1],
                ],
                columns=["a", "b", "c"],
            ),
            decomposition.PCA,
            pd.Series(["a", "b"]),
            False,
            {},
            ValueError,
        ),
        (
            pd.DataFrame(
                [[1, 1, 1]],
                columns=["a", "b", "c"],
            ),
            decomposition.PCA,
            None,
            False,
            {},
            ValueError,
        ),
    ],
)
def test_error(df, method, columns, drop, kwargs, error):
    with pytest.raises(error):
        df.decompose(method, columns, drop=drop, **kwargs)
