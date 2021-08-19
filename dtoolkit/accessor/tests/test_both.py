import pytest

from . import d
from . import s
from dtoolkit.accessor.dataframe import cols  # pylint: disable=reimported
from dtoolkit.accessor.series import cols  # pylint: disable=reimported


@pytest.mark.parametrize(
    "df, expt",
    [
        (s, s.name),
        (d, d.columns.tolist()),
    ],
)
def test_column(df, expt):
    assert df.cols() == expt
