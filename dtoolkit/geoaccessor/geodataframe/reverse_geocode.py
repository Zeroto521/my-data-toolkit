import geopandas as gpd
import pandas as pd

from dtoolkit.geoaccessor.geodataframe import drop_geometry  # noqa: F401
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

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd
    >>> df = pd.DataFrame(
    ...     {
    ...         "wkt": [
    ...             "POINT (-71.0594869 42.3584697)",
    ...             "POINT (-77.0365305 38.8977332)",
    ...         ],
    ...         "name": ["a", "b"],
    ...     },
    ... ).from_wkt("wkt", drop=True, crs=4326)
    >>> df
      name                    geometry
    0    a  POINT (-71.05949 42.35847)
    1    b  POINT (-77.03653 38.89773)
    >>> df.reverse_geocode()
      name                    geometry                                            address
    0    a  POINT (-71.05977 42.35860)  18-32, Tremont Street, 02108, Tremont Street, ...
    1    b  POINT (-77.03655 38.89772)  Pennsylvania Avenue Northwest, 20500, Pennsylv...
    """

    return pd.concat(
        (
            df.drop_geometry(),
            gpd.tools.reverse_geocode(df.geometry, **kwargs),
        ),
        axis=1,
    )
