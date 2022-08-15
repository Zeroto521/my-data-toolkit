import pandas as pd
import pytest

from dtoolkit.accessor.series import dropna_index  # noqa: F401


def test_error():
    with pytest.raises(ValueError):
        s = pd.Series([1, 2, 3, 4, 5])
        s.dropna_index(how="whatever")
