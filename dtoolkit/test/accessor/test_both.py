import pytest

from dtoolkit.accessor.dataframe import cols  # noqa
from dtoolkit.accessor.series import cols  # noqa
from dtoolkit.test.accessor import d
from dtoolkit.test.accessor import s


@pytest.mark.parametrize(
    "df, expt",
    [
        (s, s.name),
        (d, d.columns.tolist()),
    ],
)
def test_column(df, expt):
    assert df.cols() == expt
