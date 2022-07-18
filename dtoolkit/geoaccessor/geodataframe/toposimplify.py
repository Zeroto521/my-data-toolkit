from __future__ import annotations

from textwrap import dedent

import geopandas as gpd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.geoseries import toposimplify as s_toposimplify
from dtoolkit.geoaccessor.geoseries.toposimplify import _toposimplify
from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
@doc(
    s_toposimplify,
    klass=":class:`~geopandas.GeoDataFrame`",
    examples=dedent(
        """
    Examples
    --------
    .. plot::

        import dtoolkit.geoaccessor
        import geopandas as gpd
        import matplotlib.pyplot as plt


        df = (
            gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
            .query('continent == "Africa"')
        )

        fig, (ax1, ax2) = plt.subplots(ncols=2, sharex=True, sharey=True)

        df.simplify(1).plot(ax=ax1, alpha=0.7)
        df.toposimplify(1).plot(ax=ax2, alpha=0.7)

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
