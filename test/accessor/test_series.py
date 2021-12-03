from test.accessor import s
from test.accessor import s_inf

import numpy as np
import pandas as pd
import pytest

from dtoolkit.accessor.series import bin  # noqa
from dtoolkit.accessor.series import drop_inf  # noqa
from dtoolkit.accessor.series import error_report  # noqa
from dtoolkit.accessor.series import top_n  # noqa


class TestDropinf:
    def setup_method(self):
        self.s = s.copy(True)
        self.s = self.s.append(s_inf)

    @pytest.mark.parametrize(
        "inf, df, expt",
        [
            ("all", s, s),
            ("all", s.append(s_inf), s),
            ("pos", s_inf, pd.Series([-np.inf], index=[1])),
            ("neg", s_inf, pd.Series([np.inf])),
        ],
    )
    def test_work(self, inf, df, expt):
        res = df.drop_inf(inf=inf)

        assert res.equals(expt)

    def test_inplace_is_true(self):
        res = self.s.drop_inf(inplace=True)

        assert res is None
        assert self.s.equals(s)

    @pytest.mark.parametrize(
        "error, inf",
        [
            (ValueError, np.inf),
            (TypeError, None),
        ],
    )
    def test_error(self, error, inf):
        with pytest.raises(error):
            s_inf.drop_inf(inf=inf)


class TestBin:
    def setup_method(self):
        self.s = pd.Series([1, 10, 20, 30, 40, 50])

    @pytest.mark.parametrize(
        "bins, labels, right, excepted",
        [
            (
                [-np.inf, 1, 10, 20, 30, np.inf],
                ["a", "b", "c", "d", "e"],
                False,
                ["b", "c", "d", "e", "e", "e"],
            ),
            (
                [-np.inf, 1, 10, 20, 30, np.inf],
                ["a", "b", "c", "d", "e"],
                True,
                ["a", "b", "c", "d", "e", "e"],
            ),
            (
                [-np.inf, 1, 10, 20],
                ["a", "b", "c"],
                True,
                ["a", "b", "c"] + [np.nan] * 3,
            ),
            (
                [1, 10, 20],
                ["a", "b"],
                False,
                ["a", "b"] + [np.nan] * 4,
            ),
            (
                [-np.inf, np.inf],
                ["a"],
                False,
                ["a"] * 6,
            ),
        ],
    )
    def test_work(self, bins, labels, right, excepted):
        res = self.s.bin(
            bins=bins,
            labels=labels,
            right=right,
        )
        excepted = pd.Series(
            excepted,
            dtype=pd.CategoricalDtype(categories=labels),
        )

        assert res.equals(excepted)

    def test_inplace_is_true(self):
        res = self.s.bin([10, 20], ["a"], inplace=True)
        excepted = pd.Series(
            [np.nan, np.nan, "a", np.nan, np.nan, np.nan],
            dtype="category",
        )

        assert res is None
        assert self.s.equals(excepted)


class TestTopN:
    def setup_method(self):
        self.s = pd.Series(
            {
                "Italy": 59000000,
                "France": 65000000,
                "Brunei": 434000,
                "Malta": 434000,
                "Maldives": 434000,
                "Iceland": 337000,
                "Nauru": 11300,
                "Tuvalu": 11300,
                "Anguilla": 11300,
                "Montserrat": 5200,
            },
        )

    @pytest.mark.parametrize(
        "n, largest, keep, excepted",
        [
            (
                4,
                True,
                "first",
                {
                    "France": 65000000,
                    "Italy": 59000000,
                    "Brunei": 434000,
                    "Malta": 434000,
                },
            ),
            (
                4,
                True,
                "all",
                {
                    "France": 65000000,
                    "Italy": 59000000,
                    "Brunei": 434000,
                    "Malta": 434000,
                    "Maldives": 434000,
                },
            ),
            (
                2,
                False,
                "last",
                {"Montserrat": 5200, "Anguilla": 11300},
            ),
            (
                2,
                False,
                "all",
                {
                    "Montserrat": 5200,
                    "Nauru": 11300,
                    "Tuvalu": 11300,
                    "Anguilla": 11300,
                },
            ),
        ],
    )
    def test_work(self, n, largest, keep, excepted):
        result = self.s.top_n(n, largest, keep=keep)
        excepted = pd.Series(excepted)

        assert result.equals(excepted)


class TestExpand:
    @pytest.mark.parametrize(
        "suffix, delimiter, data, name, flatten, excepted",
        [
            # test default parameters
            (
                None,
                "_",
                [(1, 2), (3, 4)],
                "item",
                False,
                {
                    "item_0": [1, 3],
                    "item_1": [2, 4],
                },
            ),
            # test delimiter
            (
                None,
                "-",
                [(1, 2), (3, 4)],
                "item",
                False,
                {
                    "item-0": [1, 3],
                    "item-1": [2, 4],
                },
            ),
            # test suffix
            (
                ["a", "b"],
                "_",
                [(1, 2), (3, 4)],
                "item",
                False,
                {
                    "item_a": [1, 3],
                    "item_b": [2, 4],
                },
            ),
            # test len(suffix) > max length of elements
            (
                ["a", "b", "c"],
                "_",
                [(1, 2), (3, 4)],
                "item",
                False,
                {
                    "item_a": [1, 3],
                    "item_b": [2, 4],
                },
            ),
            # test each element length is different
            (
                None,
                "_",
                [(1, 2), (3, 4, 5)],
                "item",
                False,
                {
                    "item_0": [1, 3],
                    "item_1": [2, 4],
                    "item_2": [np.nan, 5],
                },
            ),
            # test len(suffix) > max length of elements
            (
                ["a", "b", "c", "d"],
                "_",
                [(1, 2), (3, 4, 5)],
                "item",
                False,
                {
                    "item_a": [1, 3],
                    "item_b": [2, 4],
                    "item_c": [np.nan, 5],
                },
            ),
            # test sub-element type is list-like
            (
                None,
                "_",
                [(1, 2), (3, [4, 5]), [[6]]],
                "item",
                True,
                {
                    "item_0": [1, 3, 6],
                    "item_1": [2, 4, np.nan],
                    "item_2": [np.nan, 5, np.nan],
                },
            ),
        ],
    )
    def test_work(self, suffix, delimiter, flatten, data, name, excepted):
        s = pd.Series(data, name=name)
        excepted = pd.DataFrame(excepted)

        result = s.expand(
            suffix=suffix,
            delimiter=delimiter,
            flatten=flatten,
        )

        assert result.equals(excepted)

    @pytest.mark.parametrize(
        "suffix, data, name, error",
        [
            # len(suffix) < max length of elements
            (
                ["a"],
                [(1, 2)],
                "item",
                ValueError,
            ),
            # name of series is None
            (
                None,
                [(1, 2)],
                None,
                ValueError,
            ),
        ],
    )
    def test_error(self, suffix, data, name, error):
        s = pd.Series(data, name=name)

        with pytest.raises(error):
            s.expand(suffix=suffix)

    def test_not_list_like_type(self):
        s = pd.Series([1, 2, 3])
        result = s.expand()

        assert s is result


class TestErrorReport:
    @pytest.mark.parametrize(
        "true, predicted, excepted",
        [
            # both Series
            (
                pd.Series([1, 2]),
                pd.Series([2, 1]),
                pd.DataFrame(
                    {
                        "true": [1, 2],
                        "predicted": [2, 1],
                        "absolute error": [1, 1],
                        "relative error": [1, 0.5],
                    },
                ),
            ),
            # test name
            (
                pd.Series([1, 2], name="x"),
                pd.Series([2, 1], name="y"),
                pd.DataFrame(
                    {
                        "x": [1, 2],
                        "y": [2, 1],
                        "absolute error": [1, 1],
                        "relative error": [1, 0.5],
                    },
                ),
            ),
            # predicted is array-like type
            (
                pd.Series([1, 2]),
                [2, 1],
                pd.DataFrame(
                    {
                        "true": [1, 2],
                        "predicted": [2, 1],
                        "absolute error": [1, 1],
                        "relative error": [1, 0.5],
                    },
                ),
            ),
            # predicted is array-like type
            (
                pd.Series([1, 2]),
                np.array([2, 1], dtype="int64"),
                pd.DataFrame(
                    {
                        "true": [1, 2],
                        "predicted": [2, 1],
                        "absolute error": [1, 1],
                        "relative error": [1, 0.5],
                    },
                ),
            ),
            # true has index
            (
                pd.Series([1, 2], index=["a", "b"]),
                pd.Series([2, 1], index=["a", "b"]),
                pd.DataFrame(
                    {
                        "true": [1, 2],
                        "predicted": [2, 1],
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
                pd.DataFrame(
                    {
                        "true": [1, 2],
                        "predicted": [2, 1],
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
                pd.DataFrame(
                    {
                        "true": [1, 2],
                        "predicted": [2, 1],
                        "absolute error": [1, 1],
                        "relative error": [1, 0.5],
                    },
                    index=["a", "b"],
                ),
            ),
        ],
    )
    def test_work(self, true, predicted, excepted):
        result = true.error_report(predicted)

        assert result.equals(excepted)

    @pytest.mark.parametrize(
        "true, predicted, error",
        [
            # different lengths
            (pd.Series([1, 2, 3]), pd.Series([2, 1]), IndexError),
            # different indexes
            (pd.Series([1, 2]), pd.Series([2, 1], index=["a", "b"]), IndexError),
        ],
    )
    def test_error(self, true, predicted, error):
        with pytest.raises(error):
            true.error_report(predicted)
