import pandas as pd

import pytest

from dtoolkit.accessor.series import query  # noqa: F401


@pytest.mark.parametrize(
    "s, expr, error",
    [
        (
            pd.Series(),
            list(),
            ValueError,
        ),
        (
            pd.Series(),
            tuple(),
            ValueError,
        ),
    ],
)
def test_error(s, expr, error):
    with pytest.raises(error):
        s.query(expr)
