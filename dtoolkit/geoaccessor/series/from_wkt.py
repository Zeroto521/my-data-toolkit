from __future__ import annotations

from typing import TYPE_CHECKING

import geopandas as gpd
import pandas as pd

from dtoolkit.accessor.register import register_series_method
from dtoolkit.geoaccessor.series.to_geoframe import to_geoframe


if TYPE_CHECKING:
    from pyproj import CRS


@register_series_method
def from_wkt(s: pd.Series, /, crs: CRS | str | int = None) -> gpd.GeoDataFrame:
    """
    Generate :obj:`~geopandas.GeoDataFrame` of geometries from :obj:`~pandas.Series`.

    A sugary syntax wraps :meth:`geopandas.GeoSeries.from_wkt`.

    Parameters
    ----------
    crs : CRS, str, int, optional
        Coordinate Reference System of the geometry objects. Can be anything
        accepted by :meth:`~pyproj.crs.CRS.from_user_input`, such as an authority
        string (eg "EPSG:4326" / 4326) or a WKT string.

    Returns
    -------
    GeoDataFrame

    Raises
    ------
    ValueError
        If the name of Series is empty.

    See Also
    --------
    geopandas.GeoSeries.from_wkt
    dtoolkit.geoaccessor.dataframe.from_wkt

    Notes
    -----
    This method is the accessor of Series, not GeoSeries.

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd
    >>> s = pd.Series(
    ...     [
    ...         "POINT (1 1)",
    ...         "POINT (2 2)",
    ...         "POINT (3 3)",
    ...     ],
    ...     name='wkt',
    ... )
    >>> s
    0    POINT (1 1)
    1    POINT (2 2)
    2    POINT (3 3)
    Name: wkt, dtype: object
    >>> s.from_wkt(crs=4326)
               wkt     geometry
    0  POINT (1 1)  POINT (1 1)
    1  POINT (2 2)  POINT (2 2)
    2  POINT (3 3)  POINT (3 3)
    """

    if s.name is None:
        raise ValueError(
            "to keep the original data requires setting the 'name' of "
            f"{s.__class__.__name__!r}",
        )

    return to_geoframe(s, geometry=gpd.GeoSeries.from_wkt(s, crs=crs))
