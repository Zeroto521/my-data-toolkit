import geopandas as gpd
import numpy as np
import pandas as pd

from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
def radius(s: gpd.GeoSeries, /) -> pd.Series:
    """
    Return the radius of geometry.

    Returns
    -------
    Series(float64)
        The unit is meters.

    See Also
    --------
    dtoolkit.geoaccessor.geoseries.radius
    dtoolkit.geoaccessor.geodataframe.radius

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import geopandas as gpd

    An example to get the radius of cities/provinces/countries/continents.

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
    >>> df.radius().head()
    0    7.835455e+04
    1    5.448971e+05
    2    1.754160e+05
    3    1.787487e+06
    4    1.739850e+06
    dtype: float64
    """

    return s.geoarea().divide(np.pi).apply(np.sqrt)
