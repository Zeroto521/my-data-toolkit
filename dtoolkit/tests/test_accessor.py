import numpy as np
import pandas as pd
import pytest

from dtoolkit.accessor import ColumnAccessor  # noqa
from dtoolkit.accessor import DropInfAccessor  # noqa
from dtoolkit.accessor import FilterInAccessor  # noqa


data_size = 10
s = pd.Series(range(data_size), name="item")
s = s.astype(float)

label_size = 3
d = pd.DataFrame(
    {
        "a": np.random.randint(label_size, size=data_size),
        "b": np.random.randint(label_size, size=data_size),
    },
)
s_inf = pd.Series([np.inf, -np.inf])


@pytest.mark.parametrize("df", [s, d])
def test_columnaccessor(df):
    if isinstance(df, pd.Series):
        assert df.cols() == df.name
    else:
        assert df.cols().equals(df.columns)


@pytest.mark.parametrize("df", [s, s.append(s_inf)])
def test_dropinfaccessor(df):
    assert s.equals(df.dropinf())


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
