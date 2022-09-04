import pandas as pd
import pytest
from pandas.testing import assert_index_equal

from dtoolkit.accessor.series import set_unique_index


def test_warning():
    s = pd.Series(index=[0, 0, 1, 1])

    with pytest.warns(UserWarning):
        set_unique_index(s)


@pytest.mark.parametrize(
    "s, expected",
    [
        # duplicate index
        (pd.Series(index=[0, 1, 1]), pd.Index([0, 1, 2])),
        # monotonic increasing
        (pd.Series(index=[0, 1, 2]), pd.Index([0, 1, 2])),
        (pd.Series(index=[1, 2, 3]), pd.Index([1, 2, 3])),
        # monotonic decreasing
        (pd.Series(index=[3, 2, 1]), pd.Index([0, 1, 2])),
        # non-monotonic
        (pd.Series(index=[0, 2, 1]), pd.Index([0, 1, 2])),
    ],
)
def test_work(s, expected):
    result_index = s.set_unique_index().index

    assert_index_equal(result_index, expected)
