import pytest
from dtoolkit.accessor import ColumnAccessor  # noqa

from . import d, s


@pytest.mark.parametrize(
    "df, expt",
    [
        (s, s.name),
        (d, d.columns.tolist()),
    ],
)
def test_columnaccessor(df, expt):
    assert df.cols() == expt
