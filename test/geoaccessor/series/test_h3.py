import pandas as pd
import pytest

from dtoolkit.geoaccessor.series import h3  # noqa: F401


pytest.importorskip("h3")


@pytest.mark.parametrize(
    "s, error",
    [
        # int to int
        (
            pd.Series([612845052823076863, 614269156845420543]),
            TypeError,
        ),
        # bool to int
        (
            pd.Series([True, False]),
            TypeError,
        ),
        # non-h3 str to int
        (
            pd.Series(["1", "2", "3"]),
            TypeError,
        ),
    ],
)
def test_to_int_error(s, error):
    with pytest.raises(error):
        s.h3.to_int()


@pytest.mark.parametrize(
    "s, error",
    [
        # str to str
        (
            pd.Series(["88143541bdfffff", "886528b2a3fffff"]),
            TypeError,
        ),
        # bool to str
        (
            pd.Series([True, False]),
            TypeError,
        ),
        # non-h3 int to str
        (
            pd.Series([1, 2, 3]),
            TypeError,
        ),
    ],
)
def test_to_str_error(s, error):
    with pytest.raises(error):
        s.h3.to_str()


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
        s.h3.to_points(drop=drop)


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
        s.h3.to_polygons(drop=drop)
