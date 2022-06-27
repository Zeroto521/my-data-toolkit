from typing import Hashable

import geopandas as gpd
import pandas as pd

from dtoolkit.accessor.dataframe import drop_or_not  # noqa
from dtoolkit.accessor.register import register_dataframe_method


@register_dataframe_method
def to_geocode(
    df: pd.DataFrame,
    column: Hashable,
    drop: bool = False,
    **kwargs,
) -> gpd.GeoDataFrame:
    """
    Geocode string type Series and get a GeoDataFrame of the resulting points.

    Parameters
    ----------
    column : Hashable
        The name of the column to geocode.

    drop : bool, default False
        Don't contain the original data anymore.

    **kwargs
        See the documentation for :func:`~geopandas.tools.geocode` for complete details
        on the keyword arguments.

    Returns
    -------
    GeoDataFrame


    See Also
    --------
    geopandas.tools.geocode
    dtoolkit.geoaccessor.series.to_geocode
    """

    return pd.concat(
        (
            df.drop_or_not(drop=drop, columns=column),
            gpd.tools.geocode(df[column], **kwargs),
        ),
        axis=1,
    )
