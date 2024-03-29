import pandas as pd
import pytest

from dtoolkit.transformer import RavelTF
from test.transformer.data import array
from test.transformer.data import df_iris
from test.transformer.data import s


@pytest.mark.parametrize("data", [array, df_iris, s, s.tolist()])
def test_transform(data):
    result = RavelTF().fit_transform(data)

    assert result.ndim == 1


@pytest.mark.parametrize("data", [array, df_iris, s, s.tolist()])
def test_inverse_transform(data):
    tf = RavelTF()

    transformed_data = tf.fit_transform(data)
    result = tf.inverse_transform(transformed_data)

    assert isinstance(result, pd.Series)
