from __future__ import annotations

from typing import Literal

import geopandas as gpd
from pandas.util._decorators import doc

from dtoolkit.accessor.dataframe import to_series  # noqa: F401
from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
@doc(klass="GeoSeries")
def toposimplify(
    s: gpd.GeoSeries,
    /,
    tolerance: float,
    simplify_algorithm: Literal["dp", "vw"] = "dp",
    simplify_with: Literal["shapely", "simplification"] = "shapely",
    prevent_oversimplify: bool = True,
) -> gpd.GeoSeries:
    """
    Returns a :class:`~geopandas.{klass}` containing a simplified representation
    of each geometry. Similar to :meth:`~geopandas.GeoSeries.simplify`, but keeps
    shared edges.

    .. image:: ../../../../_static/simplify-vs-toposimplify.png
        :width: 80%
        :align: center

    Parameters
    ----------
    tolerance : float
        All parts of a simplified geometry will be no more than tolerance distance from
        the original.

    simplify_algorithm : {{'dp', 'vw'}}, default 'dp'
        ``vw`` will only be selected if ``simplify_with`` is set to ``simplification``.

            - ``dp`` : Douglas-Peucker
            - ``vw`` : Visvalingam-Whyatt

    simplify_with : {{'shapely', 'simplification'}}, default 'shapely'
        Sets the package to use for simplifying. Shapely adopts solely Douglas-Peucker
        and simplification both Douglas-Peucker and Visvalingam-Whyatt. The package
        simplification is known to be quicker than shapely.

    prevent_oversimplify : bool, default True
        If `True`, the simplification is slower, but the likelihood of producing
        valid geometries is higher as it prevents oversimplification. Simplification
        happens on paths separately, so this setting is especially relevant for rings
        with no partial shared paths. This is also known as a topology-preserving
        variant of simplification.

    Returns
    -------
    {klass}

    Raises
    ------
    ModuleNotFoundError
        - If don't have module named 'topojson'.
        - If don't have module named 'simplification'.

    See Also
    --------
    geopandas.GeoSeries.simplify
    dtoolkit.geoaccessor.geoseries.toposimplify
    dtoolkit.geoaccessor.geodataframe.toposimplify
    topojson.Topology.toposimplify
        https://mattijn.github.io/topojson/api/topojson.core.topology.html#toposimplify

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import geopandas as gpd
    >>> from shapely import Point
    >>> df = gpd.GeoSeries([Point(120, 50)], crs=4326).to_geoframe().geobuffer(10)
    >>> df.geometry.iloc[0]
    <POLYGON ((120 50, 120 50, 120 50, 120 50, 120 50, 120 50, 120 50, 120 50, 1...>
    >>> df.geometry.toposimplify(1).iloc[0]
    <POLYGON ((120 50, 120 50, 120 50, 120 50, 120 50))>
    """
    from topojson import Topology

    return (
        Topology(
            s,
            toposimplify=tolerance,
            simplify_algorithm=simplify_algorithm,
            simplify_with=simplify_with,
            prevent_oversimplify=prevent_oversimplify,
        )
        .to_gdf(crs=s.crs)  # Return is a GeoDataFrame, require a GeoSeries
        .to_series()
        .set_axis(s.index)  # To fix https://github.com/mattijn/topojson/issues/164
    )
