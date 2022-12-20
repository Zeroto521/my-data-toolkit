import pandas as pd
import pytest

from dtoolkit.geoaccessor.index import h3  # noqa: F401


pytest.importorskip("h3")


@pytest.mark.parametrize(
    "index, error",
    [
        # int to int
        (
            pd.Index([612845052823076863, 614269156845420543]),
            TypeError,
        ),
        # bool to int
        (
            pd.Index([True, False]),
            TypeError,
        ),
        # non-h3 str to int
        (
            pd.Index(["1", "2", "3"]),
            TypeError,
        ),
    ],
)
def test_to_int_error(index, error):
    with pytest.raises(error):
        index.h3.to_int()


@pytest.mark.parametrize(
    "index, error",
    [
        # str to str
        (
            pd.Index(["88143541bdfffff", "886528b2a3fffff"]),
            TypeError,
        ),
        # bool to str
        (
            pd.Index([True, False]),
            TypeError,
        ),
        # non-h3 int to str
        (
            pd.Index([1, 2, 3]),
            TypeError,
        ),
    ],
)
def test_to_str_error(index, error):
    with pytest.raises(error):
        index.h3.to_str()
