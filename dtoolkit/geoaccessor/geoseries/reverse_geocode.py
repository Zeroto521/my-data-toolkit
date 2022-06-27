import geopandas as gpd
import pandas as pd

from dtoolkit.accessor.dataframe import drop_or_not  # noqa
from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
def reverse_geocode(s: gpd.GeoSeries, **kwargs) -> gpd.GeoDataFrame:
    """
    Reverse geocode Point type GeoSeries and get a GeoDataFrame of the resulting
    addresses.

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
    dtoolkit.geoaccessor.geodataframe.reverse_geocode
    """

    return gpd.tools.reverse_geocode(s.geometry, **kwargs)
