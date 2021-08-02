import numpy as np
import pandas as pd
import pytest

from dtoolkit.accessor import ColumnAccessor  # noqa
from dtoolkit.accessor import DropInfAccessor  # noqa
from dtoolkit.accessor import FilterInAccessor  # noqa
from dtoolkit.accessor import RepeatAccessor  # noqa


data_size = 42
s = pd.Series(range(data_size), name="item", dtype=float)

label_size = 3
d = pd.DataFrame(
    {
        "a": np.random.randint(label_size, size=data_size),
        "b": np.random.randint(label_size, size=data_size),
    },
    dtype=float,
)
s_inf = pd.Series([np.inf, -np.inf])


@pytest.mark.parametrize(
    "df, expt",
    [
        (s, s.name),
        (d, d.columns.tolist()),
    ],
)
def test_columnaccessor(df, expt):
    assert df.cols() == expt


class TestDropinfaccessor:
    def setup_method(self):
        self.s = s.copy(True)
        self.s = self.s.append(s_inf)

    @pytest.mark.parametrize(
        "df, expt",
        [
            (s, s),
            (s.append(s_inf), s),
            (d, d),
            (d.append({"a": np.inf}, ignore_index=True), d),
            (d.append({"b": -np.inf}, ignore_index=True), d),
        ],
    )
    def test_work(self, df, expt):
        res = df.dropinf()

        assert res.equals(expt)

    def test_inplace_is_true(self):
        res = self.s.dropinf(inplace=True)

        assert res is None
        assert self.s.equals(s)


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
        result = self.d.repeat(repeats, axis)

        assert result.equals(expected)

    @pytest.mark.parametrize("axis", [-1, 3, None])
    def test_error(self, axis):
        with pytest.raises(ValueError):
            self.d.repeat(2, axis)
