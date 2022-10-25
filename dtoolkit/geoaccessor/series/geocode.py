import geopandas as gpd
import pandas as pd

from dtoolkit.accessor.register import register_series_method


@register_series_method
def geocode(s: pd.Series, /, drop: bool = False, **kwargs) -> gpd.GeoDataFrame:
    """
    Geocode string type Series and get a GeoDataFrame of the resulting points.

    Parameters
    ----------
    drop : bool, default False
        Don't contain the original data anymore.

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

    ValueError
        If 'drop' is True and the name of Series is empty.

    See Also
    --------
    geopandas.tools.geocode
    dtoolkit.geoaccessor.dataframe.geocode

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd
    >>> s = pd.Series(
    ...     [
    ...         "boston, ma",
    ...         "1600 pennsylvania ave. washington, dc",
    ...     ],
    ... )
    >>> s
    0                               boston, ma
    1    1600 pennsylvania ave. washington, dc
    dtype: object
    >>> s.geocode(drop=True)
                         geometry                                            address
    0  POINT (-71.06051 42.35543)               Boston, Massachusetts, United States
    1  POINT (-77.03655 38.89770)  White House, 1600, Pennsylvania Avenue Northwe...
    """

    if not drop and s.name is None:
        raise ValueError(
            "to keep the original data requires setting the 'name' of "
            f"{s.__class__.__name__!r}",
        )

    df = gpd.tools.geocode(s, **kwargs)
    return df if drop else pd.concat((df, s), axis=1)
