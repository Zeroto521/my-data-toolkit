from __future__ import annotations

from typing import Hashable

import geopandas as gpd
import pandas as pd

from dtoolkit.geoaccessor.geoseries.xy import xy
from dtoolkit.geoaccessor.register import register_geoseries_method
from dtoolkit.geoaccessor.series import to_geoframe


@register_geoseries_method
def points_to_h3(
    s: gpd.GeoSeries,
    /,
    resolution: int,
    column: Hashable = "h3",
    drop: bool = True,
) -> pd.Series | gpd.GeoDataFrame:
    """
    Convert Point to containing H3 cell index.

    Parameters
    ----------
    resolution : int
        H3 resolution.

    column : Hashable, default "h3"
        Name of the column to store the H3 cell index.

    drop : bool, default True
        Whether to drop the geometry column.

    Returns
    -------
    Series or GeoDataFrame
        Series if drop is True else GeoDataFrame.

    Raises
    ------
    ModuleNotFoundError
        If don't have module named 'h3'.
    TypeError
        If the geometry is not Point.
    ValueError
        - If the CRS is not WGS84 or EPSG:4326.
        - If ``drop=False`` but ``column=None`` or ``s.name=None``.

    See Also
    --------
    h3.latlon_to_h3
    dtoolkit.geoaccessor.geoseries.points_to_h3

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd
    >>> s = pd.Series(
    ...     [
    ...         "POINT (122 55)",
    ...         "POINT (100 1)",
    ...     ],
    ... ).from_wkt(crs=4326, drop=True)
    >>> s
    0    POINT (122.00000 55.00000)
    1     POINT (100.00000 1.00000)
    dtype: geometry
    >>> s.points_to_h3(8)
    0    612845052823076863
    1    614269156845420543
    Name: h3, dtype: int64
    """

    # TODO: Use `latlon_to_h3` instead of `geo_to_h3`
    # While h3-py release 4, `latlon_to_h3` is not available.

    # requires h3 >= 4
    # from h3.api.numpy_int import latlng_to_cell
    # requires h3 < 4
    from h3.api.numpy_int import geo_to_h3

    # TODO: Advices for h3-pandas
    # 1. use `import h3.api.numpy_int as h3` instead of `import h3`
    # 2. compat with h3-py 4
    # 3. requires crs is 4326
    # 4. consider h3-py as the accessor of Series
    # 5. use h3 cell index as the index of DataFrame, this may be a problem,
    # cause it is not unique actually.
    # 6. Speed up points / polygons via pygeos

    if not all(s.geom_type == "Point"):
        raise TypeError("Only support 'Point' geometry type.")
    if s.crs != 4326:
        raise ValueError(f"Only support 'EPSG:4326' CRS, but got {s.crs!r}.")
    if not drop and (column is None or s.name is None):
        raise ValueError(
            "to keep the original data requires setting the 'name' of "
            f"{s.__class__.__name__!r} and 'column'.",
        )

    h3 = xy(s, reverse=True).apply(lambda yx: geo_to_h3(*yx, resolution)).rename(column)
    return h3 if drop else to_geoframe(h3, geometry=s)
