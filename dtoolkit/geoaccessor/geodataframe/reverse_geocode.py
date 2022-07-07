import geopandas as gpd

from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
def reverse_geocode(df: gpd.GeoDataFrame, **kwargs) -> gpd.GeoDataFrame:
    """
    Reverse geocode :obj:`~shapely.geometry.Point` type :class:`~geopandas.GeoDataFrame`
    and get the corresponding addresses.

    Parameters
    ----------
    **kwargs
        See the documentation for :func:`~geopandas.tools.reverse_geocode` for complete
        details on the keyword arguments.

    Returns
    -------
    GeoDataFrame

    Raises
    ------
    ModuleNotFoundError
        If don't have module named 'geopy'.

    See Also
    --------
    geopandas.tools.reverse_geocode
    dtoolkit.geoaccessor.dataframe.geocode
    dtoolkit.geoaccessor.geoseries.reverse_geocode
    """

    return gpd.tools.reverse_geocode(df.geometry, **kwargs)
