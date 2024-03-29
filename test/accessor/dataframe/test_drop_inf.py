import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from dtoolkit.accessor.dataframe import drop_inf  # noqa: F401
from test.accessor.data import d


@pytest.mark.parametrize(
    "df, axis, how, inf, subset, expected",
    [
        (
            d,
            0,
            "any",
            "all",
            None,
            d,
        ),
        (
            pd.concat(
                (
                    d,
                    pd.DataFrame({"a": [-np.inf]}),
                ),
                ignore_index=True,
            ),
            0,
            "any",
            "all",
            None,
            d,
        ),
        (
            pd.concat(
                (
                    d,
                    pd.DataFrame({"a": [np.inf]}),
                ),
                ignore_index=True,
            ),
            1,
            "any",
            "all",
            None,
            pd.concat(
                (
                    d,
                    pd.DataFrame({"a": [np.inf]}),
                ),
                ignore_index=True,
            ).drop(columns=["a"]),
        ),
        (
            pd.concat(
                (
                    d,
                    pd.DataFrame({"a": [np.inf]}),
                ),
                ignore_index=True,
            ),
            0,
            "all",
            "all",
            None,
            pd.concat(
                (
                    d,
                    pd.DataFrame({"a": [np.inf]}),
                ),
                ignore_index=True,
            ),
        ),
        (
            pd.concat(
                (
                    d,
                    pd.DataFrame(
                        {
                            "a": [np.inf],
                            "b": [-np.inf],
                        },
                    ),
                ),
                ignore_index=True,
            ),
            0,
            "all",
            "all",
            None,
            d,
        ),
        (
            pd.concat(
                (
                    d,
                    pd.DataFrame({"b": [-np.inf]}),
                ),
                ignore_index=True,
            ),
            0,
            "any",
            "neg",
            None,
            d,
        ),
        (
            pd.concat(
                (
                    d,
                    pd.DataFrame({"b": [-np.inf]}),
                ),
                ignore_index=True,
            ),
            0,
            "any",
            "pos",
            None,
            pd.concat(
                (
                    d,
                    pd.DataFrame({"b": [-np.inf]}),
                ),
                ignore_index=True,
            ),
        ),
        (
            pd.concat(
                (
                    d,
                    pd.DataFrame({"b": [-np.inf]}),
                ),
                ignore_index=True,
            ),
            0,
            "any",
            "all",
            ["b"],
            d,
        ),
        (
            pd.concat(
                (
                    d,
                    pd.DataFrame(
                        {
                            "b": [-np.inf],
                        },
                    ),
                ),
                ignore_index=True,
            ),
            0,
            "any",
            "all",
            ["a", "b"],
            d,
        ),
        (
            pd.concat(
                (
                    d,
                    pd.DataFrame(
                        {
                            "b": [-np.inf],
                        },
                    ),
                ),
                ignore_index=True,
            ),
            0,
            "any",
            "all",
            ["a", "b"],
            d,
        ),
    ],
)
def test_work(df, axis, how, inf, subset, expected):
    result = df.drop_inf(axis=axis, how=how, inf=inf, subset=subset)

    assert_frame_equal(result, expected)


@pytest.mark.parametrize(
    "error, axis, how, subset",
    [
        (ValueError, (0, 1), "any", None),
        (ValueError, 0, "whatever", None),
        (ValueError, 0, None, None),
        (KeyError, 0, "any", ["c"]),
    ],
)
def test_error(error, axis, how, subset):
    with pytest.raises(error):
        d.drop_inf(axis=axis, how=how, subset=subset)
