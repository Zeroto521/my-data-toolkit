from __future__ import annotations

import geopandas as gpd
import pandas as pd
from shapely import points

from dtoolkit.accessor.register import register_series_method


@register_series_method
def geocode(
    s: pd.Series,
    /,
    provider: str | "geopy.geocoder" = "photon",
    min_delay_seconds: float = 0,
    max_retries: int = 2,
    error_wait_seconds: float = 5,
    **kwargs,
) -> gpd.GeoDataFrame:
    """
    Geocode string type Series and get a GeoDataFrame of the resulting points.

    Parameters
    ----------
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

    if s.name is None:
        raise ValueError(
            "to keep the original data requires setting the 'name' of "
            f"{s.__class__.__name__!r}",
        )

    geolocate = geolocator(
        provider, True, min_delay_seconds, max_retries, error_wait_seconds, **kwargs
    )
    return s.to_geoframe(points(s.apply(query, geolocate=geolocate).tolist()), crs=4326)


def query(address: str, geolocate) -> tuple[float, float] | tuple[None, None]:
    from geopy.geocoders.base import GeocoderQueryError

    try:
        loc = geolocate(address)
        return loc.longitude, loc.latitude

    except (GeocoderQueryError, ValueError):
        return None, None


def geolocator(
    provider: str | "geopy.geocoder",
    forward: bool,
    min_delay_seconds: float,
    max_retries: int,
    error_wait_seconds: float,
    **kwargs,
):
    from geopy.extra.rate_limiter import RateLimiter
    from geopy.geocoders import get_geocoder_for_service

    # Get the actual 'geocoder' from the provider name
    if isinstance(provider, str):
        provider = get_geocoder_for_service(provider)

    return RateLimiter(
        getattr(provider(**kwargs), "geocode" if forward else "reverse"),
        min_delay_seconds=min_delay_seconds,
        max_retries=max_retries,
        error_wait_seconds=error_wait_seconds,
    )
