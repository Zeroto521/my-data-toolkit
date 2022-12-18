import pandas as pd
import pytest

from dtoolkit.accessor.series.to_zh import to_zh


pytest.importorskip("zhconv")


@pytest.mark.parametrize(
    "s, error",
    [
        (
            pd.Series([1, 2]),
            TypeError,
        ),
    ],
)
def test_error(s, error):
    with pytest.raises(error):
        to_zh(s)
