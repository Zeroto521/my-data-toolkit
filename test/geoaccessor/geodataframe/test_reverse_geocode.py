import pytest

gpd = pytest.importorskip("geopandas")

import pandas as pd

from dtoolkit.geoaccessor.geodataframe import reverse_geocode  # noqa: F401


def test_type():
    df = pd.Series(
        [
            "POINT (-71.0594869 42.3584697)",
            "POINT (-77.0365305 38.8977332)",
        ],
        name="WKT",
    ).from_wkt(crs=4326)
    result = df.reverse_geocode()

    assert isinstance(result, gpd.GeoDataFrame)
