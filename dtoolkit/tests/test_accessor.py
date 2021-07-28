import numpy as np
import pandas as pd
import pytest

from dtoolkit.accessor import ColumnAccessor  # noqa
from dtoolkit.accessor import DropInfAccessor  # noqa
from dtoolkit.accessor import FilterInAccessor  # noqa


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


@pytest.mark.parametrize("df", [s, d])
def test_columnaccessor(df):
    if isinstance(df, pd.Series):
        assert df.cols() == df.name
    else:
        assert df.cols().equals(df.columns)


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
