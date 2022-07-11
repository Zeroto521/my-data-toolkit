import geopandas as gpd
import pandas as pd

from dtoolkit.geoaccessor.dataframe import from_wkb  # noqa: F401
from dtoolkit.geoaccessor.dataframe import from_wkt  # noqa: F401


def test_csv():
    file = "wkb.csv"
    (
        pd.DataFrame(
            {
                "wkt": [
                    "POINT (1 1)",
                    "POINT (2 2)",
                    "POINT (3 3)",
                ],
            },
        )
        .from_wkt("wkt", crs=4326)
        .to_wkb()
        .to_csv(file, index=False)
    )

    df = (
        pd.read_csv(file)
        .assign(geometry=lambda df: df.geometry.apply(eval))
        .from_wkb("geometry")
    )

    assert isinstance(df, gpd.GeoDataFrame)
    assert isinstance(df.geometry, gpd.GeoSeries)
