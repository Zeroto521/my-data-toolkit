import pytest

import pandas as pd

from dtoolkit.accessor.series import set_unique_index


def test_warning():
    s = pd.Series(index=[0, 0, 1, 1])

    with pytest.warns(UserWarning):
        set_unique_index(s)
