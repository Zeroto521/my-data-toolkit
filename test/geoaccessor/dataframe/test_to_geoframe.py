import pandas as pd
from pandas.testing import assert_frame_equal

from dtoolkit.geoaccessor.dataframe import to_geoframe  # noqa: F401


def test_original_dataframe_type():
    df = pd.DataFrame(
        pd.DataFrame(
            {
                "wkt": [
                    "POINT (1 1)",
                    "POINT (2 2)",
                    "POINT (3 3)",
                ],
            },
        )
        .from_wkt("wkt")
        .rename_geometry("geom"),
    )

    df_copy = df.copy()
    df.to_geoframe(geometry=df["geom"])

    assert_frame_equal(df, df_copy)
