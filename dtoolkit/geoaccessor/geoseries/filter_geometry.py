from __future__ import annotations

from typing import TYPE_CHECKING, Literal, get_args

import geopandas as gpd
import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.register import register_geoseries_method


if TYPE_CHECKING:
    from shapely.geometry.base import BaseGeometry


BINARY_PREDICATE = Literal[
    "intersects",
    "disjoint",
    "crosses",
    "overlaps",
    "touches",
    "covered_by",
    "contains",
    "within",
    "covers",
]


@register_geoseries_method
@doc(klass="GeoSeries")
def filter_geometry(
    s: gpd.GeoSeries,
    /,
    geometry: BaseGeometry | gpd.GeoSeries | gpd.GeoDataFrame,
    predicate: BINARY_PREDICATE,
    complement: bool = False,
    **kwargs,
) -> pd.Series:
    """
    Filter {klass} by ``geometry``.

    A sugar syntax wraps::

        s[s.{{predicate}}(geometry, **kwargs)]

    Parameters
    ----------
    geometry : Geometry, GeoSeries, or GeoDataFrame

    predicate : {{"intersects", "disjoint", "crosses", "overlaps", "touches", \
"covered_by", "contains", "within", "covers"}}
        Binary predicate.

    complement : bool, default False
        If True, do operation reversely.

    **kwargs
        See the documentation for ``{klass}.{{predicate}}`` for complete details on the
        keyword arguments.

    Returns
    -------
    {klass}

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import geopandas as gpd
    >>> from shapely.geometry import Polygon, LineString, Point, box
    >>> df = gpd.GeoDataFrame(
    ...     geometry=[
    ...         Polygon([(0, 0), (1, 1), (0, 1)]),
    ...         LineString([(0, 0), (0, 2)]),
    ...         LineString([(0, 0), (0, 1)]),
    ...         Point(0, 1),
    ...     ],
    ... )
    >>> df
                                                geometry
    0  POLYGON ((0.00000 0.00000, 1.00000 1.00000, 0....
    1      LINESTRING (0.00000 0.00000, 0.00000 2.00000)
    2      LINESTRING (0.00000 0.00000, 0.00000 1.00000)
    3                            POINT (0.00000 1.00000)
    4                          POINT (-1.00000 -1.00000)

    Filter the geometries out of the bounding box ``box(0, 0, 2, 2)``.

    >>> df.filter_geometry(box(0, 0, 2, 2), "covered_by")
                          geometry
    4    POINT (-1.00000 -1.00000)
    """

    return s[
        _filter_geometry(
            s,
            geometry=geometry,
            predicate=predicate,
            complement=complement,
            **kwargs,
        )
    ]


def _filter_geometry(
    s: gpd.GeoSeries,
    geometry: BaseGeometry | gpd.GeoSeries | gpd.GeoDataFrame,
    predicate: BINARY_PREDICATE,
    complement: bool,
    **kwargs,
) -> pd.Series:
    if predicate not in get_args(BINARY_PREDICATE):
        raise ValueError(
            f"Got {predicate=!r}, expected one of {get_args(BINARY_PREDICATE)!r}."
        )

    mask = getattr(s, predicate)(geometry, **kwargs)
    return ~mask if complement else mask
