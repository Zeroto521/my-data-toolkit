import dtoolkit._compat as compat
from . import need_dependency

if compat.HAS_SKLEARN:
    import pandas as pd
    import pytest

    from . import array
    from . import df_iris
    from . import s
    from dtoolkit.transformer import RavelTF


@need_dependency
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

        assert isinstance(res, pd.DataFrame)
