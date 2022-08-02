import geopandas as gpd
import pandas as pd

from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
def geoarea(df: gpd.GeoDataFrame, /) -> pd.Series:
    """
    Returns a ``Series`` containing the **geographic area** (m^2) of each geometry.

    A sugar syntax wraps::

        s.to_crs({"proj": "cea"}).area

    Returns
    -------
    Series
    """

    return df.to_crs({"proj": "cea"}).area
