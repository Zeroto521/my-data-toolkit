import geopandas as gpd
from pandas.util._decorators import doc
from shapely import Point

from dtoolkit.geoaccessor.geoseries import geocentroid as s_geocentroid
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
@doc(s_geocentroid)
def geocentroid(
    df: gpd.GeoDataFrame,
    /,
    max_iter: int = 500,
    tol: float = 1e-5,
) -> Point:

    return s_geocentroid(df.geometry, max_iter=max_iter, tol=tol)
