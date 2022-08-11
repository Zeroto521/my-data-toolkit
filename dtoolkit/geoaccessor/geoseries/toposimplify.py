from __future__ import annotations

from typing import Literal

import geopandas as gpd
from pandas.util._decorators import doc

from dtoolkit.accessor.dataframe import to_series  # noqa: F401
from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
@doc(klass=":class:`~geopandas.GeoSeries`")
def toposimplify(
    s: gpd.GeoSeries,
    /,
    tolerance: float,
    simplify_algorithm: Literal["dp", "vw"] = "dp",
    simplify_with: Literal["shapely", "simplification"] = "shapely",
    prevent_oversimplify: bool = True,
) -> gpd.GeoSeries:
    """
    Returns a {klass} containing a simplified representation of each geometry.
    Similar to :func:`~geopandas.GeoSeries.simplify`, but keeps shared edges.

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
    >>> df = (
    ...     gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    ...     .query('continent == "Africa"')
    ... )
    >>> df.head()
           pop_est  ...                                           geometry
    1   58005463.0  ...  POLYGON ((33.90371 -0.95000, 34.07262 -1.05982...
    2     603253.0  ...  POLYGON ((-8.66559 27.65643, -8.66512 27.58948...
    11  86790567.0  ...  POLYGON ((29.34000 -4.49998, 29.51999 -5.41998...
    12  10192317.3  ...  POLYGON ((41.58513 -1.68325, 40.99300 -0.85829...
    13  52573973.0  ...  POLYGON ((39.20222 -4.67677, 37.76690 -3.67712...
    <BLANKLINE>
    [5 rows x 6 columns]
    >>> df.toposimplify(0.1).head()
           pop_est  ...                                           geometry
    1   58005463.0  ...  POLYGON ((-8.66561 27.65644, -8.81786 27.65644...
    2     603253.0  ...  POLYGON ((29.33999 -4.50001, 29.27634 -3.29391...
    11  86790567.0  ...  POLYGON ((19.89576 -24.76780, 19.89542 -21.849...
    12  10192317.3  ...  POLYGON ((-16.71374 13.59499, -15.62454 13.623...
    13  52573973.0  ...  POLYGON ((-11.51397 12.44302, -11.45617 12.076...
    <BLANKLINE>
    [5 rows x 6 columns]
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
        # `to_gdf` return is a GeoDataFrame, require GeoSeries
        .to_gdf(crs=s.crs).to_series()
    )
