from __future__ import annotations

from typing import Literal

import geopandas as gpd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.geoseries import toposimplify as s_toposimplify
from dtoolkit.geoaccessor.geoseries.toposimplify import _toposimplify
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
@doc(s_toposimplify, klass=":class:`~geopandas.GeoDataFrame`")
def toposimplify(
    df: gpd.GeoDataFrame,
    /,
    tolerance: float,
    simplify_algorithm: Literal["dp", "vw"] = "dp",
    simplify_with: Literal["shapely", "simplification"] = "shapely",
    prevent_oversimplify: bool = False,
) -> gpd.GeoDataFrame:

    return _toposimplify(
        df,
        tolerance,
        simplify_algorithm,
        simplify_with,
        prevent_oversimplify,
    )
