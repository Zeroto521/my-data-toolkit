from __future__ import annotations

from typing import TYPE_CHECKING

import geopandas as gpd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.geoseries import filter_geometry as s_filter_geometry
from dtoolkit.geoaccessor.geoseries.filter_geometry import _filter_geometry
from dtoolkit.geoaccessor.geoseries.filter_geometry import BINARY_PREDICATE
from dtoolkit.geoaccessor.register import register_geodataframe_method


if TYPE_CHECKING:
    from shapely.geometry.base import BaseGeometry


@register_geodataframe_method
@doc(s_filter_geometry, klass="GeoDataFrame")
def filter_geometry(
    df: gpd.GeoDataFrame,
    /,
    other: BaseGeometry | gpd.GeoSeries | gpd.GeoDataFrame,
    predicate: BINARY_PREDICATE,
    complement: bool = False,
    **kwargs,
) -> gpd.GeoDataFrame:

    return df[
        _filter_geometry(
            df,
            other=other,
            predicate=predicate,
            complement=complement,
            **kwargs,
        )
    ]
