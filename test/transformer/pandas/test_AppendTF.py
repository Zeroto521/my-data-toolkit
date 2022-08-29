import pandas as pd
from pandas.testing import assert_series_equal

from dtoolkit.transformer import AppendTF


def test_work():
    tf = AppendTF(other=pd.DataFrame(dict(a=range(1, 9))), ignore_index=True)

    result = tf.fit_transform(pd.DataFrame(dict(a=[0])))
    expected = pd.Series(range(9), name="a")

    assert_series_equal(result, expected)
