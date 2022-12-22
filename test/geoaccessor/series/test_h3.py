import pandas as pd
import pytest

from dtoolkit.geoaccessor.series import H3


pytest.importorskip("h3")


@pytest.mark.parametrize(
    "s, drop, error",
    [
        # without name
        (
            pd.Series([612845052823076863, 614269156845420543]),
            False,
            ValueError,
        ),
        # not H3 int
        (
            pd.Series([1, 2]),
            True,
            TypeError,
        ),
    ],
)
def test_to_points_error(s, drop, error):
    with pytest.raises(error):
        H3(s).to_points(drop=drop)


@pytest.mark.parametrize(
    "s, drop, error",
    [
        # without name
        (
            pd.Series([612845052823076863, 614269156845420543]),
            False,
            ValueError,
        ),
        # not H3 int
        (
            pd.Series([1, 2]),
            True,
            TypeError,
        ),
    ],
)
def test_to_polygons_error(s, drop, error):
    with pytest.raises(error):
        H3(s).to_polygons(drop=drop)
