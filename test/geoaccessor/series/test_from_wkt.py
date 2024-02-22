import pandas as pd
import pytest

from dtoolkit.geoaccessor.series import from_wkt


@pytest.mark.parametrize(
    "s, error",
    [
        (
            pd.Series(
                [
                    "POINT (1 1)",
                    "POINT (2 2)",
                    "POINT (3 3)",
                ],
            ),
            ValueError,
        ),
    ],
)
def test_error(s, error):
    with pytest.raises(error):
        from_wkt(s)
