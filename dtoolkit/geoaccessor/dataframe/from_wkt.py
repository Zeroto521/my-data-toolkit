from __future__ import annotations

from typing import Hashable
from typing import TYPE_CHECKING

import geopandas as gpd
import pandas as pd

from dtoolkit.accessor.register import register_dataframe_method
from dtoolkit.geoaccessor.dataframe.to_geoframe import to_geoframe


if TYPE_CHECKING:
    from pyproj import CRS


@register_dataframe_method
def from_wkt(
    df: pd.DataFrame,
    /,
    geometry: Hashable,
    crs: CRS | str | int = None,
) -> gpd.GeoDataFrame:
    """
    Generate :obj:`~geopandas.GeoDataFrame` of geometries from 'WKT' column of
    :obj:`~pandas.DataFrame`.

    A sugary syntax wraps :meth:`geopandas.GeoSeries.from_wkt`.

    Parameters
    ----------
    geometry : Hashable
        The name of WKT column.

    crs : CRS, str, int, optional
        Coordinate Reference System of the geometry objects. Can be anything
        accepted by :meth:`~pyproj.crs.CRS.from_user_input`, such as an authority
        string (eg "EPSG:4326" / 4326) or a WKT string.

    Returns
    -------
    GeoDataFrame

    See Also
    --------
    geopandas.GeoSeries.from_wkt
    dtoolkit.geoaccessor.series.from_wkt
    dtoolkit.geoaccessor.dataframe.from_xy
    dtoolkit.geoaccessor.dataframe.from_wkb

    Notes
    -----
    This method is the accessor of DataFrame, not GeoDataFrame.

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd
    >>> df = pd.DataFrame(
    ...     {
    ...         "wkt": [
    ...             "POINT (1 1)",
    ...             "POINT (2 2)",
    ...             "POINT (3 3)",
    ...         ]
    ...     }
    ... )
    >>> df
               wkt
    0  POINT (1 1)
    1  POINT (2 2)
    2  POINT (3 3)
    >>> df.from_wkt("wkt", crs=4326)
               wkt     geometry
    0  POINT (1 1)  POINT (1 1)
    1  POINT (2 2)  POINT (2 2)
    2  POINT (3 3)  POINT (3 3)
    """

    # Avoid mutating the original DataFrame.
    # https://github.com/geopandas/geopandas/issues/1179
    return to_geoframe(
        df.copy(),
        geometry=gpd.GeoSeries.from_wkt(df[geometry]),
        crs=crs,
    )
