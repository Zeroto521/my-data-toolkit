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
    >>> from shapely import Point
    >>> df = gpd.GeoSeries([Point(120, 50)], crs=4326).to_geoframe().geobuffer(10)
    >>> df
                                                geometry
    0  POLYGON ((120.00014 50, 120.00014 49.99999, 12...
    >>> df.radius()
    0    9.990294
    dtype: float64
    """

    return s.geoarea().divide(np.pi).apply(np.sqrt)
