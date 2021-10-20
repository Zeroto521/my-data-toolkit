import pandas as pd
import pytest

from dtoolkit.test.transformer import array
from dtoolkit.test.transformer import df_iris
from dtoolkit.test.transformer import s
from dtoolkit.transformer import RavelTF


class TestRavelTF:
    @pytest.mark.parametrize("data", [array, df_iris, s, s.tolist()])
    def test_transform(self, data):
        res = RavelTF().fit_transform(data)

        assert res.ndim == 1

    @pytest.mark.parametrize("data", [array, df_iris, s, s.tolist()])
    def test_inverse_transform(self, data):
        tf = RavelTF()

        transformed_data = tf.fit_transform(data)
        res = tf.inverse_transform(transformed_data)

        assert isinstance(res, pd.Series)
