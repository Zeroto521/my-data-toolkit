from textwrap import dedent

import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.geoseries import count_coordinates as s_count_coordinates
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
@doc(
    s_count_coordinates,
    klass=":class:`~geopandas.GeoDataFrame`",
    examples=dedent(
        """
    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import geopandas as gpd
    >>> d = gpd.GeoSeries.from_wkt(["POINT (0 0)", "LINESTRING (2 2, 4 4)", None])
    >>> d = d.to_frame("geometry")
    >>> d
                                            geometry
    0                        POINT (0.00000 0.00000)
    1  LINESTRING (2.00000 2.00000, 4.00000 4.00000)
    2                                           None
    >>> d.count_coordinates()
    0    1
    1    2
    2    0
    Name: geometry, dtype: int64
    """,
    ),
)
def count_coordinates(df: gpd.GeoDataFrame) -> pd.Series:
    return df.geometry.count_coordinates()
