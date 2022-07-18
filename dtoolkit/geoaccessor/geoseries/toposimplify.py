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
    plot=dedent(
        """
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
    prevent_oversimplify: bool = True,
) -> gpd.GeoSeries:
    """
    Apply :func:`topojson.Topology.toposimplify` to {klass} to keep **shared edges**.

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
         pop_est continent             name iso_a3  gdp_md_est                                           geometry  # noqa: E501
    1   53950935    Africa         Tanzania    TZA    150600.0  POLYGON ((33.90371 -0.95000, 34.07262 -1.05982...  # noqa: E501
    2     603253    Africa        W. Sahara    ESH       906.5  POLYGON ((-8.66559 27.65643, -8.66512 27.58948...  # noqa: E501
    11  83301151    Africa  Dem. Rep. Congo    COD     66010.0  POLYGON ((29.34000 -4.49998, 29.51999 -5.41998...  # noqa: E501
    12   7531386    Africa          Somalia    SOM      4719.0  POLYGON ((41.58513 -1.68325, 40.99300 -0.85829...  # noqa: E501
    13  47615739    Africa            Kenya    KEN    152700.0  POLYGON ((39.20222 -4.67677, 37.76690 -3.67712...  # noqa: E501
    >>> df.toposimplify(0.1).head()
                                                geometry   pop_est continent             name iso_a3  gdp_md_est  # noqa: E501
    0  POLYGON ((33.90367 -0.95000, 30.76984 -1.01452...  53950935    Africa         Tanzania    TZA    150600.0  # noqa: E501
    1  POLYGON ((-8.66561 27.65644, -8.79490 27.12073...    603253    Africa        W. Sahara    ESH       906.5  # noqa: E501
    2  POLYGON ((29.33999 -4.50001, 29.27634 -3.29391...  83301151    Africa  Dem. Rep. Congo    COD     66010.0  # noqa: E501
    3  POLYGON ((41.58509 -1.68324, 42.04156 -0.91918...   7531386    Africa          Somalia    SOM      4719.0  # noqa: E501
    4  POLYGON ((39.20220 -4.67675, 39.60493 -4.34650...  47615739    Africa            Kenya    KEN    152700.0  # noqa: E501
    {plot}
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
    simplify_algorithm: Literal["dp", "vw"],
    simplify_with: Literal["shapely", "simplification"],
    prevent_oversimplify: bool,
) -> gpd.GeoSeries | gpd.GeoDataFrame:
    from topojson import Topology

    return Topology(
        gpd_obj,
        toposimplify=tolerance,
        simplify_algorithm=simplify_algorithm,
        simplify_with=simplify_with,
        prevent_oversimplify=prevent_oversimplify,
    ).to_gdf(crs=gpd_obj.crs)
