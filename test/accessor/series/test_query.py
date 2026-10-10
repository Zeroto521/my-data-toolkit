import pandas as pd
import pytest

from dtoolkit.accessor.series import query  # noqa: F401


@pytest.mark.parametrize(
    "s, expr, error",
    [
        (
            pd.Series(),
            [],
            TypeError,
        ),
        (
            pd.Series(),
            (),
            TypeError,
        ),
    ],
)
def test_error(s, expr, error):
    with pytest.raises(error):
        s.query(expr)
