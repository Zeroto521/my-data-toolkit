import numpy as np
import pandas as pd
import pytest

from . import d
from dtoolkit.accessor import DropInfDataFrameAccessor  # noqa
from dtoolkit.accessor import FilterInAccessor  # noqa
from dtoolkit.accessor import RepeatAccessor  # noqa


class TestDropinfDataFrameAccessor:
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
    def test_work(self, df, axis, how, inf, subset, expt):
        res = df.dropinf(axis=axis, how=how, inf=inf, subset=subset)

        assert res.equals(expt)

    @pytest.mark.parametrize(
        "error, axis, how, subset",
        [
            (TypeError, (0, 1), "any", None),
            (ValueError, 0, "whatever", None),
            (TypeError, 0, None, None),
            (KeyError, 0, "any", ["c"]),
        ],
    )
    def test_error(self, error, axis, how, subset):
        with pytest.raises(error):
            d.dropinf(axis=axis, how=how, subset=subset)

    def test_inplace_is_true(self):
        self_d = d.copy(True)
        self_d = self_d.append(
            {
                "a": np.inf,
                "b": -np.inf,
            },
            ignore_index=True,
        )
        res = self_d.dropinf(inplace=True)

        assert res is None
        assert self_d.equals(d)


class TestFilterInAccessor:
    def setup_method(self):
        self.d = d.copy(True)
        self.condition = {"a": [0, 1], "b": [2]}

    def test_work(self):
        res = self.d.filterin(self.condition)

        assert res["a"].isin([0, 1]).any()  # 0 and 1 in a
        assert (~res["a"].isin([2])).all()  # 2 not in a
        assert res["b"].isin([2]).any()  # 2 in a
        assert (~res["b"].isin([0, 1])).all()  # 0 and not in a

    def test_inplace_is_true(self):
        res = self.d.filterin(self.condition, inplace=True)

        assert res is None
        assert self.d.equals(d) is False


class TestRepeatAccessor:
    def setup_method(self):
        self.d = pd.DataFrame({"a": [1, 2], "b": [3, 4]})

    @pytest.mark.parametrize(
        "repeats, axis, expected",
        [
            (1, 0, pd.DataFrame({"a": [1, 2], "b": [3, 4]})),
            (1, 1, pd.DataFrame({"a": [1, 2], "b": [3, 4]})),
            (
                2,
                0,
                pd.DataFrame(
                    {
                        "a": [1, 1, 2, 2],
                        "b": [3, 3, 4, 4],
                    },
                    index=[0, 0, 1, 1],
                ),
            ),
            (
                2,
                1,
                pd.DataFrame(
                    [
                        [1, 1, 3, 3],
                        [2, 2, 4, 4],
                    ],
                    columns=["a", "a", "b", "b"],
                ),
            ),
            (
                [1, 2],
                1,
                pd.DataFrame(
                    [
                        [1, 3, 3],
                        [2, 4, 4],
                    ],
                    columns=["a", "b", "b"],
                ),
            ),
        ],
    )
    def test_work(self, repeats, axis, expected):
        result = self.d.repeat(repeats, axis=axis)

        assert result.equals(expected)

    @pytest.mark.parametrize("axis", [-1, 3, None])
    def test_error(self, axis):
        with pytest.raises(ValueError):
            self.d.repeat(2, axis)
