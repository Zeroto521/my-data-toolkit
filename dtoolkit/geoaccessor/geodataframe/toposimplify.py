from __future__ import annotations

from typing import Literal

import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.dataframe import to_geoframe  # noqa: F401
from dtoolkit.geoaccessor.geodataframe import drop_geometry
from dtoolkit.geoaccessor.geoseries import toposimplify as s_toposimplify
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
@doc(s_toposimplify, klass=":class:`~geopandas.GeoDataFrame`")
def toposimplify(
    df: gpd.GeoDataFrame,
    /,
    tolerance: float,
    simplify_algorithm: Literal["dp", "vw"] = "dp",
    simplify_with: Literal["shapely", "simplification"] = "shapely",
    prevent_oversimplify: bool = True,
) -> gpd.GeoDataFrame:

    return pd.concat(
        (
            drop_geometry(df),
            s_toposimplify(
                df.geometry,
                tolerance,
                simplify_algorithm,
                simplify_with,
                prevent_oversimplify,
            ),
        ),
        axis=1,
    ).to_geoframe()
