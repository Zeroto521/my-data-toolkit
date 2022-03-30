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
            d.append({"a": np.inf}, ignore_index=True),
            0,
            "any",
            "all",
            None,
            d,
        ),
        (
            d.append({"a": np.inf}, ignore_index=True),
            1,
            "any",
            "all",
            None,
            d.append({"a": np.inf}, ignore_index=True).drop(columns=["a"]),
        ),
        (
            d.append({"a": np.inf}, ignore_index=True),
            0,
            "all",
            "all",
            None,
            d.append({"a": np.inf}, ignore_index=True),
        ),
        (
            d.append({"a": np.inf, "b": -np.inf}, ignore_index=True),
            0,
            "all",
            "all",
            None,
            d,
        ),
        (
            d.append({"b": -np.inf}, ignore_index=True),
            0,
            "any",
            "neg",
            None,
            d,
        ),
        (
            d.append({"b": -np.inf}, ignore_index=True),
            0,
            "any",
            "pos",
            None,
            d.append({"b": -np.inf}, ignore_index=True),
        ),
        (
            d.append({"b": -np.inf}, ignore_index=True),
            0,
            "any",
            "all",
            ["b"],
            d,
        ),
        (
            d.append({"b": -np.inf}, ignore_index=True),
            0,
            "any",
            "all",
            ["a", "b"],
            d,
        ),
        (
            d.append({"b": -np.inf}, ignore_index=True),
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
