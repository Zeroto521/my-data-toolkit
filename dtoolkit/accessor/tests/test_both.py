import pytest

from . import d
from . import s
from dtoolkit.accessor import ColumnAccessor  # noqa


@pytest.mark.parametrize(
    "df, expt",
    [
        (s, s.name),
        (d, d.columns.tolist()),
    ],
)
def test_columnaccessor(df, expt):
    assert df.cols() == expt
