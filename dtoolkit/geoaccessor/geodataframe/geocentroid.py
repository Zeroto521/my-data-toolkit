from typing import Hashable

import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc
from shapely import Point

from dtoolkit.geoaccessor.geoseries import geocentroid as s_geocentroid
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
@doc(s_geocentroid)
def geocentroid(
    df: gpd.GeoDataFrame,
    /,
    weights: Hashable | pd.Series = None,
    max_iter: int = 300,
    tol: float = 1e-5,
) -> Point:
    if weights is not None and isinstance(weights, Hashable):
        weights = df[weights]

    return s_geocentroid(df.geometry, weights=weights, max_iter=max_iter, tol=tol)
