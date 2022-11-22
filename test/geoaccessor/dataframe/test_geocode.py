import geopandas as gpd
import pandas as pd
import pytest

from dtoolkit.geoaccessor.dataframe import geocode  # noqa: F401


pytest.importorskip("geopy")


def test_type():
    df = pd.DataFrame(
        {
            "name": [
                "boston, ma",
                "1600 pennsylvania ave. washington, dc",
            ],
        },
    )
    result = df.geocode("name", drop=True)

    assert isinstance(result, gpd.GeoDataFrame)
