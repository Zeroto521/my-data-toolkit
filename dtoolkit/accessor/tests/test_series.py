import numpy as np
import pandas as pd
import pytest

from . import s
from . import s_inf
from dtoolkit.accessor.series import dropinf  # noqa
from dtoolkit.accessor.series import range_replace  # noqa


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


class TestRangeReplace:
    def setup_method(self):
        self.s = pd.Series([1, 10, 20, 30, 40, 50])

    @pytest.mark.parametrize(
        "to_replace, equal_sign, excepted",
        [
            (
                {
                    (-np.inf, 1): "a",
                    (1, 10): "b",
                    (10, 20): "c",
                    (20, 30): "d",
                    (30, np.inf): "e",
                },
                "left",
                ["b", "c", "d", "e", "e", "e"],
            ),
            (
                {
                    (-np.inf, 1): "a",
                    (1, 10): "b",
                    (10, 20): "c",
                    (20, 30): "d",
                    (30, np.inf): "e",
                },
                "right",
                ["a", "b", "c", "d", "e", "e"],
            ),
            (
                {
                    (-np.inf, 1): "a",
                    (1, 10): "b",
                    (10, 20): "c",
                },
                "right",
                ["a", "b", "c", 30, 40, 50],
            ),
            (
                {
                    (1, 10): "a",
                    (10, 20): "b",
                },
                "left",
                ["a", "b", 20, 30, 40, 50],
            ),
            (
                {
                    (-np.inf, np.inf): "a",
                },
                "left",
                ["a"] * 6,
            ),
            (
                {
                    (np.inf, -np.inf): "a",
                },
                "left",
                [1, 10, 20, 30, 40, 50],
            ),
        ],
    )
    def test_work(self, to_replace, equal_sign, excepted):
        res = self.s.range_replace(
            to_replace=to_replace,
            equal_sign=equal_sign,
        )
        excepted = pd.Series(excepted, index=self.s.index)

        assert res.equals(excepted)

    def test_inplace_is_true(self):
        res = self.s.range_replace({(10, 20): None}, inplace=True)

        assert res is None
        assert self.s.equals(pd.Series([1, None, 20, 30, 40, 50]))
