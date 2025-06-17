import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
@doc(alias="s")
def geoarea(s: gpd.GeoSeries, /) -> pd.Series:
    r"""
    Returns a ``Series`` containing the **geographic area** (m\ :sup:`2`) of each
    geometry.

    A sugar syntax wraps::

        {alias}.to_crs("+proj=cea").area

    Returns
    -------
    Series(float64)

    See Also
    --------
    geopandas.GeoSeries.area
    dtoolkit.geoaccessor.geoseries.geoarea
    dtoolkit.geoaccessor.geodataframe.geoarea

    Notes
    -----
    The result is a tiny bit different from the value, because of CRS problem. But the
    `cea`_ (Equal Area Cylindrical) CRS is quite enough, the average absolute error is
    less than 0.04% base on 'naturalearth_lowres' data.

    .. _cea: https://proj.org/operations/projections/cea.html

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import geopandas as gpd
    >>> from shapely import Polygon
    >>> df = gpd.GeoDataFrame(
    ...     geometry=[
    ...         Polygon([(0,0), (1,0), (1,1), (0,1)]),
    ...         Polygon([(1,1), (2,1), (2,2), (1,2)]),
    ...         Polygon([(2,2), (3,2), (3,3), (2,3)]),
    ...         Polygon([(2, 0), (3, 0), (3, 1)]),
    ...     ],
    ...     crs="EPSG:4326",
    ... )
    >>> df.geoarea()
    0    1.230846e+10
    1    1.230481e+10
    2    1.229752e+10
    3    6.154232e+09
    dtype: float64
    """

    return s.to_crs("+proj=cea").area
