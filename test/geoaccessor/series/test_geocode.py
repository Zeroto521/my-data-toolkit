import pandas as pd
import pytest

from dtoolkit.geoaccessor.series import geocode  # noqa


@pytest.mark.parametrize(
    "s, drop, error",
    [
        (
            pd.Series(
                [
                    "boston, ma",
                    "1600 pennsylvania ave. washington, dc",
                ],
            ),
            False,
            ValueError,
        ),
    ],
)
def test_error(s, drop, error):
    with pytest.raises(error):
        s.geocode(drop=drop)
