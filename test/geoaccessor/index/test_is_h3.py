import pandas as pd
import pytest

from dtoolkit.geoaccessor.index import is_h3


pytest.importorskip("h3")


@pytest.mark.parametrize(
    "index, error",
    [
        (pd.Index([True, False]), TypeError),
    ],
)
def test_error(index, error):
    with pytest.raises(error):
        is_h3(index)
