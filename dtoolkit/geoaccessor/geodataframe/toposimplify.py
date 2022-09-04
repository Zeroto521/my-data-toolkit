from __future__ import annotations

from typing import Literal

import geopandas as gpd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.geoseries import toposimplify as s_toposimplify
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
@doc(s_toposimplify, klass="GeoDataFrame")
def toposimplify(
    df: gpd.GeoDataFrame,
    /,
    tolerance: float,
    simplify_algorithm: Literal["dp", "vw"] = "dp",
    simplify_with: Literal["shapely", "simplification"] = "shapely",
    prevent_oversimplify: bool = True,
) -> gpd.GeoDataFrame:

    return df.assign(
        **{
            df.geometry.name: s_toposimplify(
                df.geometry,
                tolerance=tolerance,
                simplify_algorithm=simplify_algorithm,
                simplify_with=simplify_with,
                prevent_oversimplify=prevent_oversimplify,
            ),
        }
    )
