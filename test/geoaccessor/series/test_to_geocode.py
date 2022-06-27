from dtoolkit.geoaccessor.series import to_geocode  # noqa
import pandas as pd

import pytest


@pytest.mark.parametrize(
    "s, drop, error",
    [
        (
            pd.Series(
                [
                    "boston, ma",
                    "1600 pennsylvania ave. washington, dc",
                ]
            ),
            False,
            ValueError,
        ),
    ],
)
def test_error(s, drop, error):
    with pytest.raises(error):
        s.to_geocode(drop=drop)
