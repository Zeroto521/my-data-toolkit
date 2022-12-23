import pandas as pd
from pandas.testing import assert_frame_equal

from dtoolkit.geoaccessor.dataframe import from_wkt


def test_original_dataframe_type():
    df = pd.DataFrame(
        {
            "wkt": [
                "POINT (1 1)",
                "POINT (2 2)",
                "POINT (3 3)",
            ],
        },
    )
    df_copy = df.copy()
    from_wkt(df, "wkt")

    assert_frame_equal(df, df_copy)
