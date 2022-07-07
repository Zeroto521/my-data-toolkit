import pandas as pd
import pytest

from dtoolkit.geoaccessor.series import from_wkb  # noqa


@pytest.mark.parametrize(
    "s, drop, error",
    [
        (
            pd.Series(
                [
                    b"\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf0?\x00\x00\x00\x00\x00\x00\xf0?",  # noqa
                    b"\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x00@",  # noqa
                    b"\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08@\x00\x00\x00\x00\x00\x00\x08@",  # noqa
                ],
            ),
            False,
            ValueError,
        ),
    ],
)
def test_error(s, drop, error):
    with pytest.raises(error):
        s.from_wkb(drop=drop)
