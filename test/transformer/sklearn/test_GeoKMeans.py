import numpy as np
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


@pytest.mark.parametrize(
    "X, init, expected",
    [
        (
            [
                [113.615822, 37.844797],
                [113.586288, 37.917018],
                [113.630711, 37.865369],
                [113.590684, 37.948056],
                [113.631483, 37.862634],
                [113.57413, 37.968669],
                [113.663159, 37.848446],
                [113.586941, 37.868116],
                [113.679381, 37.875028],
                [113.5706, 37.973542],
                [113.585504, 37.879261],
                [113.584412, 37.935521],
                [113.575964, 37.906472],
                [113.593658, 37.848911],
                [113.633605, 37.869107],
                [113.582298, 37.857025],
                [113.629378, 37.805196],
                [113.48768, 37.872603],
                [113.477766, 37.868846],
            ],
            "k-means++",
            [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0],
        ),
        (
            [
                [113.615822, 37.844797],
                [113.586288, 37.917018],
                [113.630711, 37.865369],
                [113.590684, 37.948056],
                [113.631483, 37.862634],
                [113.57413, 37.968669],
                [113.663159, 37.848446],
                [113.586941, 37.868116],
                [113.679381, 37.875028],
                [113.5706, 37.973542],
                [113.585504, 37.879261],
                [113.584412, 37.935521],
                [113.575964, 37.906472],
                [113.593658, 37.848911],
                [113.633605, 37.869107],
                [113.582298, 37.857025],
                [113.629378, 37.805196],
                [113.48768, 37.872603],
                [113.477766, 37.868846],
            ],
            "random",
            [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0],
        ),
    ],
)
def test_init_paramter(X, init, expected):
    result = GeoKMeans(n_clusters=2, init=init, random_state=0, n_init="auto").fit(X)

    assert result.labels_.tolist() == expected


def test_transform():
    result = (
        GeoKMeans(
            n_clusters=2,
            random_state=0,
            n_init="auto",
        )
        .fit_transform(np.asarray([[-180, -90], [180, 90]]))
        .tolist()
    )

    assert result == [[0.0, 3.141592653589793], [3.141592653589793, 0.0]]
