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
    Series

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
    >>> df = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    >>> df.head()
           pop_est  ...                                           geometry
    0     889953.0  ...  MULTIPOLYGON (((180.00000 -16.06713, 180.00000...
    1   58005463.0  ...  POLYGON ((33.90371 -0.95000, 34.07262 -1.05982...
    2     603253.0  ...  POLYGON ((-8.66559 27.65643, -8.66512 27.58948...
    3   37589262.0  ...  MULTIPOLYGON (((-122.84000 49.00000, -122.9742...
    4  328239523.0  ...  MULTIPOLYGON (((-122.84000 49.00000, -120.0000...
    <BLANKLINE>
    [5 rows x 6 columns]
    >>> df.geoarea().head()
    0    1.928760e+10
    1    9.327793e+11
    2    9.666925e+10
    3    1.003773e+13
    4    9.509851e+12
    dtype: float64
    """

    return s.to_crs("+proj=cea").area
