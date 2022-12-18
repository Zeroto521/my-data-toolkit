import pandas as pd
import pytest

from dtoolkit.geoaccessor.geodataframe import to_h3


pytest.importorskip("h3")


@pytest.mark.parametrize(
    "df, resolution, drop, name, error",
    [
        # crs != 4326
        (
            pd.DataFrame({"x": [122, 100], "y": [55, 1]}).from_xy("x", "y"),
            8,
            True,
            None,
            ValueError,
        ),
        # geometry type is not Point or Polygon
        (
            pd.DataFrame(
                {
                    "label": ["a", "b"],
                    "wkt": [
                        "LINESTRING (122 100, 55 1)",
                        "LINESTRING (122 55, 100 1)",
                    ],
                },
            ).from_wkt("wkt", crs=4326, drop=True),
            8,
            True,
            None,
            TypeError,
        ),
    ],
)
def test_error(df, resolution, drop, name, error):
    with pytest.raises(error):
        to_h3(df, resolution=resolution, drop=drop, name=name)
