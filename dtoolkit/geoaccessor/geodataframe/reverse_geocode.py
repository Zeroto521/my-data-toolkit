import geopandas as gpd
import pandas as pd

from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
def reverse_geocode(df: gpd.GeoDataFrame, **kwargs) -> gpd.GeoDataFrame:
    """
    Reverse geocode Point type GeoDataFrame and get a GeoDataFrame of the resulting addresses.

    Parameters
    ----------
    **kwargs
        See the documentation for :func:`~geopandas.tools.geocode` for complete details
        on the keyword arguments.

    Returns
    -------
    GeoDataFrame

    Raises
    ------
    ModuleNotFoundError
        If don't have module named 'geopy'.

    See Also
    --------
    dtoolkit.geoaccessor.series.geocode
    dtoolkit.geoaccessor.dataframe.geocode
    dtoolkit.geoaccessor.geoseries.reverse_geocode
    """

    return gpd.tools.reverse_geocode(df.geometry, **kwargs)
