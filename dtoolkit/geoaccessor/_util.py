from __future__ import annotations

from warnings import warn

from pyproj import CRS


def string_or_int_to_crs(
    crs: str | None = None,
    epsg: int | None = None,
) -> CRS:
    if crs is not None:
        return CRS.from_user_input(crs)
    elif epsg is not None:
        return CRS.from_epsg(epsg)

    warn(
        "The crs is missing, and the crs would be set 'EPSG:4326'.",
        UserWarning,
    )
    return CRS.from_epsg(4326)
