import geopandas as gpd
import pandas as pd
from pandas.testing import assert_frame_equal

from dtoolkit.geoaccessor.dataframe import from_wkb
from dtoolkit.geoaccessor.dataframe import from_wkt


def test_csv():
    file = "wkb.csv"
    (
        from_wkt(
            pd.DataFrame(
                {
                    "wkt": [
                        "POINT (1 1)",
                        "POINT (2 2)",
                        "POINT (3 3)",
                    ],
                },
            ),
            "wkt",
            crs=4326,
        )
        .to_wkb()
        .to_csv(file, index=False)
    )

    df = pd.read_csv(file).assign(geometry=lambda df: df.geometry.apply(eval))
    df_copy = df.copy()
    result = from_wkb(df, "geometry")

    # test the original data is not changed
    assert_frame_equal(df, df_copy)
    assert isinstance(result, gpd.GeoDataFrame)
    assert isinstance(result.geometry, gpd.GeoSeries)
