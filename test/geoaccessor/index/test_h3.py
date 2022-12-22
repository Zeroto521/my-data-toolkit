import pandas as pd
import pytest
from pandas.testing import assert_index_equal
from pandas._libs.reshape import explode

from dtoolkit.geoaccessor.index import H3


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
        H3(index).to_int()


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
        H3(index).to_str()


@pytest.mark.parametrize(
    "index, expected",
    [
        (
            pd.Index([612845052823076863]),
            pd.Index(
                [
                    617348652448612351,
                    617348652448874495,
                    617348652449136639,
                    617348652449398783,
                    617348652449660927,
                    617348652449923071,
                    617348652450185215,
                ],
            ),
        ),
        (
            pd.Index([614269156845420543]),
            pd.Index(
                [
                    618772756470956031,
                    618772756471218175,
                    618772756471480319,
                    618772756471742463,
                    618772756472004607,
                    618772756472266751,
                    618772756472528895,
                ],
            ),
        ),
    ],
)
def test_to_children(index, expected):
    result, _ = explode(H3(index).to_children().to_numpy())
    result = pd.Index(result, dtype=index.dtype)

    assert_index_equal(result, expected)
