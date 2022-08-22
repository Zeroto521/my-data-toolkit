import pytest

pytest.importorskip("geopandas")

import pandas as pd

from dtoolkit.geoaccessor.geoseries.duplicated_geometry_groups import set_unique_index


def test_warning():
    s = pd.Series(list("abcd"), index=[0, 0, 1, 2])

    with pytest.warns(UserWarning):
        set_unique_index(s)
