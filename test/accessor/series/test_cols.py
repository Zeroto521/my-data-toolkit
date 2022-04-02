from test.accessor.conftest import d
from test.accessor.conftest import s

import pytest

from dtoolkit.accessor.dataframe import cols  # noqa
from dtoolkit.accessor.series import cols  # noqa


@pytest.mark.parametrize(
    "df, expt",
    [
        (s, s.name),
        (d, d.columns.tolist()),
    ],
)
def test_work(df, expt):
    assert df.cols() == expt
