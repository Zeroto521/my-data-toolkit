import pytest

from dtoolkit.transformer import GeoKMeans


@pytest.mark.parametrize(
    "X, error",
    [
        (
            # ndim != 2
            [[0, 0, 0]],
            ValueError,
        ),
        (
            # ndim != 2
            [[0]],
            ValueError,
        ),
        (
            # ndim = 2 but longitude is not right
            [[181, 0]],
            ValueError,
        ),
        (
            # ndim = 2 but longitude is not right
            [[-181, 0]],
            ValueError,
        ),
        (
            # ndim = 2 but latitude is not right
            [[0, 91]],
            ValueError,
        ),
        (
            # ndim = 2 but latitude is not right
            [[0, -91]],
            ValueError,
        ),
    ],
)
def test_validate_coordinate(X, error):
    with pytest.raises(error):
        GeoKMeans().fit(X)
