from __future__ import annotations

from typing import Hashable
from typing import TYPE_CHECKING

import geopandas as gpd
import pandas as pd

from dtoolkit.accessor.register import register_dataframe_method
from dtoolkit.geoaccessor.dataframe.to_geoframe import to_geoframe
from dtoolkit.util._decorator import warning

if TYPE_CHECKING:
    from pyproj import CRS


@register_dataframe_method("points_from_xy")
@register_dataframe_method
@warning(
    "The keyword argument 'drop' is deprecated, please use "
    "'.drop(columns=[...])' method instead. (Warning added DToolKit 0.0.20)",
    category=DeprecationWarning,
    stacklevel=3,
)
def from_xy(
    df: pd.DataFrame,
    /,
    x: Hashable,
    y: Hashable,
    z: Hashable = None,
    crs: CRS | str | int = None,
) -> gpd.GeoDataFrame:
    """
    Generate :obj:`~geopandas.GeoDataFrame` of :obj:`~shapely.geometry.Point`
    geometries from columns of :obj:`~pandas.DataFrame`.

    A sugary syntax wraps :meth:`geopandas.points_from_xy`.

    Parameters
    ----------
    x : Hashable
        ``df``'s column name.

    y : Hashable
        ``df``'s column name.

    z : Hashable, optional
        ``df``'s column name.

    crs : CRS, str, int, optional
        Coordinate Reference System of the geometry objects. Can be anything
        accepted by :meth:`~pyproj.crs.CRS.from_user_input`, such as an authority
        string (eg "EPSG:4326" / 4326) or a WKT string.

    drop : bool, default False
        Don't contain ``x``, ``y`` and ``z`` columns anymore.

        .. deprecated:: 0.0.20
            If you want to drop ``x``, ``y`` and ``z`` columns, please use
            ``.drop(columns=[...])`` method instead.

    Returns
    -------
    GeoDataFrame

    See Also
    --------
    geopandas.points_from_xy
    geopandas.GeoSeries.from_xy
    dtoolkit.geoaccessor.dataframe.from_wkt

    Notes
    -----
    - This method is the accessor of DataFrame, not GeoDataFrame.
    - This method could be called via ``df.points_from_xy`` or ``df.from_xy``.

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd
    >>> df = pd.DataFrame({"x": [122, 100], "y":[55, 1]})
    >>> df
         x   y
    0  122  55
    1  100   1
    >>> df.from_xy("x", "y", crs="EPSG:4326")
         x   y                    geometry
    0  122  55  POINT (122.00000 55.00000)
    1  100   1   POINT (100.00000 1.00000)
    """

    # Avoid mutating the original DataFrame.
    # https://github.com/geopandas/geopandas/issues/1179
    return to_geoframe(
        df.copy(),
        geometry=gpd.points_from_xy(
            df[x],
            df[y],
            z=df[z] if z is not None else z,
            crs=crs,
        ),
    )
