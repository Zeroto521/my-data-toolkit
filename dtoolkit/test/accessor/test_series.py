import numpy as np
import pandas as pd
import pytest

from . import s
from . import s_inf
from dtoolkit.accessor.series import bin  # noqa
from dtoolkit.accessor.series import dropinf  # noqa


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
        res = df.dropinf(inf=inf)

        assert res.equals(expt)

    def test_inplace_is_true(self):
        res = self.s.dropinf(inplace=True)

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
            s_inf.dropinf(inf=inf)


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
