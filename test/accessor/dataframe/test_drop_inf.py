from test.accessor.conftest import d

import numpy as np
import pandas as pd
import pytest

import dtoolkit.accessor.dataframe  # noqa


@pytest.mark.parametrize(
    "df, axis, how, inf, subset, expt",
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
def test_work(df, axis, how, inf, subset, expt):
    res = df.drop_inf(axis=axis, how=how, inf=inf, subset=subset)

    assert res.equals(expt)


@pytest.mark.parametrize(
    "error, axis, how, subset",
    [
        (ValueError, (0, 1), "any", None),
        (ValueError, 0, "whatever", None),
        (TypeError, 0, None, None),
        (KeyError, 0, "any", ["c"]),
    ],
)
def test_error(error, axis, how, subset):
    with pytest.raises(error):
        d.drop_inf(axis=axis, how=how, subset=subset)


def test_inplace_is_true():
    self_d = d.copy(True)
    self_d = self_d.append(
        {
            "a": np.inf,
            "b": -np.inf,
        },
        ignore_index=True,
    )
    res = self_d.drop_inf(inplace=True)

    assert res is None
    assert self_d.equals(d)
