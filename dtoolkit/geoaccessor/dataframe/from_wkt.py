from __future__ import annotations

from typing import TYPE_CHECKING

import geopandas as gpd
import pandas as pd

from dtoolkit._typing import IntOrStr
from dtoolkit.accessor.dataframe import drop_or_not  # noqa
from dtoolkit.accessor.dataframe import to_series  # noqa
from dtoolkit.accessor.register import register_dataframe_method

if TYPE_CHECKING:
    from pyproj import CRS


@register_dataframe_method()
def from_wkt(
    df: pd.DataFrame,
    column: str,
    crs: CRS | IntOrStr = None,
    drop: bool = False,
) -> gpd.GeoSeries | gpd.GeoDataFrame:
    """
    Generate :obj:`~geopandas.GeoDataFrame` of :obj:`~shapely.geometry.Point`
    geometries from columns of :obj:`~pandas.DataFrame`.

    A sugary syntax wraps :meth:`geopandas.GeoSeries.from_wkt`.

    Parameters
    ----------
    column : str
        The name of WKT column.

    crs : CRS, str, int, optional
        Coordinate Reference System of the geometry objects. Can be anything
        accepted by :meth:`~pyproj.crs.CRS.from_user_input`, such as an authority
        string (eg "EPSG:4326" / 4326) or a WKT string.

    drop : bool, default False
        Don't contain ``x``, ``y`` and ``z`` anymore.

    Returns
    -------
    GeoSeries or GeoDataFrame
        GeoSeries if dropped ``df`` is empty else GeoDataFrame.

    See Also
    --------
    geopandas.GeoSeries.from_wkt
    dtoolkit.geoaccessor.dataframe.from_xy

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
               wkt                 geometry
    0  POINT (1 1)  POINT (1.00000 1.00000)
    1  POINT (2 2)  POINT (2.00000 2.00000)
    2  POINT (3 3)  POINT (3.00000 3.00000)

    Drop original 'wkt' column.

    >>> df.from_wkt("wkt", drop=True)
    0    POINT (1.00000 1.00000)
    1    POINT (2.00000 2.00000)
    2    POINT (3.00000 3.00000)
    Name: geometry, dtype: geometry
    """

    return gpd.GeoDataFrame(
        df.drop_or_not(drop=drop, columns=column),
        geometry=gpd.GeoSeries.from_wkt(df[column]),
        crs=crs,
    ).to_series()
