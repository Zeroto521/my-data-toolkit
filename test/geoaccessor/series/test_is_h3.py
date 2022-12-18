import pandas as pd
import pytest

from dtoolkit.geoaccessor.series import is_h3


pytest.importorskip("h3")


@pytest.mark.parametrize(
    "s, error",
    [
        (pd.Series([True, False]), TypeError),
    ],
)
def test_error(s, error):
    with pytest.raises(error):
        is_h3(s)
