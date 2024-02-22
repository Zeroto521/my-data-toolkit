import pandas as pd
import pytest

from dtoolkit.geoaccessor.series import H3


pytest.importorskip("h3")


@pytest.mark.parametrize(
    "s, error",
    [
        # without name
        (
            pd.Series([612845052823076863, 614269156845420543]),
            ValueError,
        ),
    ],
)
def test_to_points_error(s, error):
    with pytest.raises(error):
        H3(s).to_points()


@pytest.mark.parametrize(
    "s, error",
    [
        # without name
        (
            pd.Series([612845052823076863, 614269156845420543]),
            ValueError,
        ),
    ],
)
def test_to_polygons_error(s, error):
    with pytest.raises(error):
        H3(s).to_polygons()
