import geopandas as gpd
import pandas as pd

from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
def geoarea(s: gpd.GeoSeries, /) -> pd.Series:
    """
    Returns a ``Series`` containing the **geographic area** (m^2) of each geometry.

    A sugar syntax wraps::

        s.to_crs({"proj": "cea"}).area

    Returns
    -------
    Series
    """

    return s.to_crs({"proj": "cea"}).area
