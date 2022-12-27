from typing import Hashable

import geopandas as gpd
import pandas as pd

from dtoolkit.accessor.register import register_dataframe_method
from dtoolkit.geoaccessor.series import geocode as s_geocode


@register_dataframe_method
def geocode(
    df: pd.DataFrame,
    /,
    provider: str | "geopy.geocoder" = "photon",
    min_delay_seconds: float = 0,
    max_retries: int = 2,
    error_wait_seconds: float = 5,
    **kwargs,
) -> gpd.GeoDataFrame:
    """
    Geocode a string type column from a DataFrame and get a GeoDataFrame of the
    resulting points.

    Parameters
    ----------
    address : Hashable
        The name of the column to geocode.

    provider : str or geopy.geocoder, default "photon"
        Specifies geocoding service to use. Default will use "photon", see the Photon's
        terms of service at: https://photon.komoot.io. Either the string name used by
        geopy (as specified in ``geopy.geocoders.SERVICE_TO_GEOCODER``) or a geopy
        Geocoder instance (e.g., :obj:`~geopy.geocoders.Photon`) may be used. Some
        providers require additional arguments such as access keys, please see each
        geocoder's specific parameters in :mod:`geopy.geocoders`.

    min_delay_seconds, max_retries, error_wait_seconds
        See the documentation for :func:`~geopy.extra.rate_limiter.RateLimiter` for
        complete details on these arguments.

    **kwargs
        Additional keyword arguments to pass to the geocoder.

    Returns
    -------
    GeoDataFrame

    Raises
    ------
    ModuleNotFoundError
        If don't have module named 'geopy'.

    See Also
    --------
    geopandas.tools.geocode
    dtoolkit.geoaccessor.series.geocode

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd
    >>> df = pd.DataFrame(
    ...     {
    ...         "address": [
    ...             "boston, ma",
    ...             "1600 pennsylvania ave. washington, dc",
    ...         ],
    ...     }
    ... )
    >>> df
                                     address
    0                             boston, ma
    1  1600 pennsylvania ave. washington, dc
    >>> df.geocode("address")
                                                 address                    geometry
    0               Boston, Massachusetts, United States  POINT (-71.06051 42.35543)
    1  White House, 1600, Pennsylvania Avenue Northwe...  POINT (-77.03655 38.89770)
    """

    return pd.concat(
        (
            df.drop(columns=address),
            s_geocode(
                df[address],
                provider=provider,
                min_delay_seconds=min_delay_seconds,
                max_retries=max_retries,
                error_wait_seconds=error_wait_seconds,
                **kwargs,
            ),
        ),
        axis=1,
    ).to_geoframe()
