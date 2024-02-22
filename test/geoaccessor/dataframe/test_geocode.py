import geopandas as gpd
import pandas as pd
import pytest

from dtoolkit.geoaccessor.dataframe import geocode


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
    result = geocode(df, "name")

    assert isinstance(result, gpd.GeoDataFrame)
