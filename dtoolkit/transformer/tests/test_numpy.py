import pytest

from . import array
from . import df_iris
from . import s
from dtoolkit.transformer import RavelTF

#
# Create dataset
#


@pytest.mark.parametrize("data", [array, df_iris, s, s.tolist()])
def test_raveltf(data):
    res = RavelTF().fit_transform(data)

    assert res.ndim == 1
