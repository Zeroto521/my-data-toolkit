import pytest

gpd = pytest.importorskip("geopandas")

import pandas as pd

from dtoolkit.geoaccessor.series import geocode  # noqa: F401


@pytest.mark.parametrize(
    "s, drop, error",
    [
        (
            pd.Series(
                [
                    "boston, ma",
                    "1600 pennsylvania ave. washington, dc",
                ],
            ),
            False,
            ValueError,
        ),
    ],
)
def test_error(s, drop, error):
    with pytest.raises(error):
        s.geocode(drop=drop)


def test_type():
    s = pd.Series(
        [
            "boston, ma",
            "1600 pennsylvania ave. washington, dc",
        ],
        name="address",
    )

    result = s.geocode()

    assert isinstance(result, gpd.GeoDataFrame)
