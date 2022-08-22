import pytest

pytest.importorskip("sklearn")

import pandas as pd

from dtoolkit.transformer import FillnaTF


def test_fill0():
    df = pd.DataFrame({"a": [None, 1], "b": [1, None]})
    tf = FillnaTF(0)
    result = tf.fit_transform(df)

    assert None not in result
