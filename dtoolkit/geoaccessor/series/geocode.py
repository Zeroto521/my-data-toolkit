from __future__ import annotations

from typing import Hashable
from typing import TYPE_CHECKING

import geopandas as gpd
import pandas as pd
from shapely import Point

from dtoolkit.accessor.register import register_series_method

if TYPE_CHECKING:
    import geopy.geocoders


@register_series_method
def geocode(
    s: pd.Series,
    /,
    address: Hashable = "address",
    provider: str | geopy.geocoder = "photon",
    min_delay_seconds: float = 0,
    max_retries: int = 2,
    error_wait_seconds: float = 5,
    **kwargs,
) -> gpd.GeoDataFrame:
    """
    Geocode Series(string) and get a GeoDataFrame of the resulting points.

    Parameters
    ----------
    address : Hashable
        The name of the column to geocode.

        .. note::
            This parameter only works for DataFrame.

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
    dtoolkit.geoaccessor.dataframe.geocode

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
    0                             boston, ma  POINT (-71.06051 42.35543)
    1  1600 pennsylvania ave. washington, dc  POINT (-77.03655 38.89770)
    """

    if s.name is None:
        raise ValueError(
            "to keep the original data requires setting the 'name' of "
            f"{s.__class__.__name__!r}",
        )

    geolocate = geolocator(
        provider,
        True,
        min_delay_seconds,
        max_retries,
        error_wait_seconds,
        **kwargs,
    )
    return s.to_geoframe(s.apply(query, geolocate=geolocate), crs=4326)


def query(address: str, geolocate) -> None | Point:
    from geopy.geocoders.base import GeocoderQueryError

    try:
        loc = geolocate(address)
        return Point(loc.longitude, loc.latitude)

    except (GeocoderQueryError, ValueError, AttributeError):
        return None


def geolocator(
    provider: str | geopy.geocoder,
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
