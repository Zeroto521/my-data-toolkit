from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Hashable

import geopandas as gpd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.register import register_geoseries_method
from dtoolkit.geoaccessor.series.geocode import geolocator

if TYPE_CHECKING:
    import geopy.geocoders


@register_geoseries_method
@doc(klass="GeoSeries")
def reverse_geocode(
    s: gpd.GeoSeries,
    /,
    provider: str | geopy.geocoder = "photon",
    address: Hashable = "address",
    min_delay_seconds: float = 0,
    max_retries: int = 2,
    error_wait_seconds: float = 5,
    **kwargs,
) -> gpd.GeoDataFrame:
    """
    Reverse geocode :obj:`~shapely.geometry.Point` type :class:`~geopandas.{klass}`
    and get the corresponding addresses.

    Parameters
    ----------
    provider : str or geopy.geocoder, default "photon"
        Specifies geocoding service to use. Default will use "photon", see the Photon's
        terms of service at: https://photon.komoot.io. Either the string name used by
        geopy (as specified in ``geopy.geocoders.SERVICE_TO_GEOCODER``) or a geopy
        Geocoder instance (e.g., :obj:`~geopy.geocoders.Photon`) may be used. Some
        providers require additional arguments such as access keys, please see each
        geocoder's specific parameters in :mod:`geopy.geocoders`.

    address : Hashable, default "address"
        The name of the column to store the address.

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
        If the CRS is not ``ESGP:4326``.

    See Also
    --------
    geopandas.tools.reverse_geocode
    dtoolkit.geoaccessor.series.geocode
    dtoolkit.geoaccessor.dataframe.geocode
    dtoolkit.geoaccessor.geoseries.reverse_geocode
    dtoolkit.geoaccessor.geodataframe.reverse_geocode

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd
    >>> df = (
    ...     pd.Series(
    ...         [
    ...             "POINT (-71.0594869 42.3584697)",
    ...         ],
    ...         name="wkt",
    ...     )
    ...     .from_wkt(crs=4326)
    ...     .geometry.to_geoframe()
    ... )
    >>> df
                         geometry
    0  POINT (-71.05949 42.35847)
    >>> df.reverse_geocode()
                         geometry                                            address
    0  POINT (-71.05977 42.35860)  18-32, Tremont Street, 02108, Tremont Street, ...
    """

    if s.crs != 4326:
        raise ValueError(f"Only support 'EPSG:4326' CRS, but got {s.crs!r}.")

    geolocate = geolocator(
        provider, False, min_delay_seconds, max_retries, error_wait_seconds, **kwargs
    )
    return (
        s.xy(reverse=True, frame=False, name=address)
        .apply(query, geolocate=geolocate)
        .to_geoframe(s)
    )


def query(point: tuple[float, float], geolocate) -> str | None:
    from geopy.geocoders.base import GeocoderQueryError

    try:
        return geolocate(point).address

    except (GeocoderQueryError, ValueError):
        return None
