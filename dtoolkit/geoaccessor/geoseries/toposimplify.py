from __future__ import annotations

from textwrap import dedent
from typing import Literal

import geopandas as gpd
from pandas.util._decorators import doc

from dtoolkit.accessor.dataframe import to_series  # noqa: F401
from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
@doc(
    klass=":class:`~geopandas.GeoSeries`",
    seealso=dedent(
        """
    See Also
    --------
    geopandas.GeoSeries.simplify
    topojson.Topology.toposimplify
        https://mattijn.github.io/topojson/api/topojson.core.topology.html#toposimplify
    dtoolkit.geoaccessor.geodataframe.toposimilify
    """,
    ),
    examples=dedent(
        """
    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import geopandas as gpd
    >>> import matplotlib.pyplot as plt
    >>> df = (
    ...     gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    ...     .query('continent == "Africa"')
    ... )
    >>> fig, (ax1, ax2) = plt.subplots(ncols=2, sharex=True, sharey=True)
    >>> df.geometry.simplify(1).plot(ax=ax1, alpha=0.7)
    >>> df.geometry.toposimplify(1).plot(ax=ax2, alpha=0.7)
    >>> ax1.set_title("simplify")
    >>> ax1.set_axis_off()
    >>> ax2.set_title("toposimplify")
    >>> ax2.set_axis_off()
    >>> fig.tight_layout()
    >>> plt.show()

    .. plot::

        import dtoolkit.geoaccessor
        import geopandas as gpd
        import matplotlib.pyplot as plt


        df = (
            gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
            .query('continent == "Africa"')
        )

        fig, (ax1, ax2) = plt.subplots(ncols=2, sharex=True, sharey=True)

        df.geometry.simplify(1).plot(ax=ax1, alpha=0.7)
        df.geometry.toposimplify(1).plot(ax=ax2, alpha=0.7)

        ax1.set_title("simplify")
        ax1.set_axis_off()
        ax2.set_title("toposimplify")
        ax2.set_axis_off()
        fig.tight_layout()
        plt.show()
    """,
    ),
)
def toposimplify(
    s: gpd.GeoSeries,
    /,
    tolerance: float,
    simplify_algorithm: Literal["dp", "vw"] = "dp",
    simplify_with: Literal["shapely", "simplification"] = "shapely",
    prevent_oversimplify: bool = False,
) -> gpd.GeoSeries:
    """
    Apply :func:`topojson.Topology.toposimplify` to {klass} to keep **shared edges**.

    Parameters
    ----------
    tolerance : float
        tolerance parameter.

    simplify_algorithm : {{'dp', 'vw'}}, default 'dp'
        Choose between `dp` and `vw`, for Douglas-Peucker or Visvalingam-Whyatt
        respectively. `vw` will only be selected if `simplify_with` is set to
        `simplification`.

    simplify_with : {{'shapely', 'simplification'}}, default 'shapely'
        Sets the package to use for simplifying. Shapely adopts solely Douglas-Peucker
        and simplification both Douglas-Peucker and Visvalingam-Whyatt. The pacakge
        simplification is known to be quicker than shapely.

    prevent_oversimplify : bool, default False
        If this setting is set to `True`, the simplification is slower, but the
        likelihood of producing valid geometries is higher as it prevents
        oversimplification. Simplification happens on paths separately, so this
        setting is especially relevant for rings with no partial shared paths. This
        is also known as a topology-preserving variant of simplification.

    Returns
    -------
    {klass}

    Raises
    ------
    ModuleNotFoundError
        - If don't have module named 'topojson'.
        - If don't have module named 'simplification'.
    {seealso}
    {examples}
    """

    return s.pipe(
        _toposimplify,
        tolerance,
        simplify_algorithm,
        simplify_with,
        prevent_oversimplify,
    ).to_series()


def _toposimplify(
    gpd_obj: gpd.GeoSeries | gpd.GeoDataFrame,
    tolerance: float,
    simplify_algorithm: Literal["dp", "vw"] = "dp",
    simplify_with: Literal["shapely", "simplification"] = "shapely",
    prevent_oversimplify: bool = False,
) -> gpd.GeoSeries | gpd.GeoDataFrame:
    from topojson import Topology

    return Topology(
        gpd_obj,
        toposimplify=tolerance,
        simplify_algorithm=simplify_algorithm,
        simplify_with=simplify_with,
        prevent_oversimplify=prevent_oversimplify,
    ).to_gdf(crs=gpd_obj.crs)
