import numpy as np
import pandas as pd
import pandas._testing as tm
import pytest
from pyproj import CRS

from dtoolkit.geoaccessor._util import is_int_or_float
from dtoolkit.geoaccessor._util import string_or_int_to_crs


class TestStringOrIntToCRS:
    @pytest.mark.parametrize("crs", [None, "epsg:4326"])
    @pytest.mark.parametrize("epsg", [None, 4326])
    def test_to_crs_work(self, crs, epsg):
        c = string_or_int_to_crs(crs, epsg)
        assert isinstance(c, CRS)

    def test_to_crs_missing(self):
        with tm.assert_produces_warning(UserWarning) as w:
            string_or_int_to_crs()

        msg = str(w[0].message)
        assert "missing" in msg
        assert "EPSG:4326" in msg


@pytest.mark.parametrize(
    "var, expected",
    [
        (1, True),
        (1.0, True),
        (np.array([1, 1.0])[0], True),
        (np.array([1, 1.0])[1], True),
        (np.array([1, 1.0]), False),
        (pd.Series(), False),
        (pd.DataFrame(), False),
        ([], False),
        (None, False),
    ],
)
def test_is_int_or_float(var, expected):
    assert is_int_or_float(var) is expected
