import pandas as pd
import pytest

from dtoolkit.geoaccessor.series import from_wkb


@pytest.mark.parametrize(
    "s, error",
    [
        (
            pd.Series(
                [
                    b"\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf0?\x00\x00\x00\x00\x00\x00\xf0?",  # noqa: E501
                    b"\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x00@",  # noqa: E501
                    b"\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08@\x00\x00\x00\x00\x00\x00\x08@",  # noqa: E501
                ],
            ),
            ValueError,
        ),
    ],
)
def test_error(s, error):
    with pytest.raises(error):
        from_wkb(s)
