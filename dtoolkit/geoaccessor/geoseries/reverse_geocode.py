import geopandas as gpd

from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
def reverse_geocode(s: gpd.GeoSeries, /, **kwargs) -> gpd.GeoDataFrame:
    """
    Reverse geocode :obj:`~shapely.geometry.Point` type :class:`~geopandas.GeoSeries`
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
    dtoolkit.geoaccessor.series.geocode
    dtoolkit.geoaccessor.geodataframe.reverse_geocode

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd
    >>> s = pd.Series(
    ...     [
    ...         "POINT (-71.0594869 42.3584697)",
    ...         "POINT (-77.0365305 38.8977332)",
    ...     ],
    ... ).from_wkt(drop=True, crs=4326)
    >>> s
    0    POINT (-71.05949 42.35847)
    1    POINT (-77.03653 38.89773)
    dtype: geometry
    >>> s.reverse_geocode()
                         geometry                                            address
    0  POINT (-71.05977 42.35860)  18-32, Tremont Street, 02108, Tremont Street, ...
    1  POINT (-77.03655 38.89772)  1600, Pennsylvania Avenue Northwest, 20500, Pe...
    """

    return gpd.tools.reverse_geocode(s.geometry, **kwargs)
