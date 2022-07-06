from typing import Hashable

import geopandas as gpd
import pandas as pd

from dtoolkit.accessor import register_dataframe_method
from dtoolkit.accessor.dataframe import drop_or_not  # noqa


@register_dataframe_method
def geocode(
    df: pd.DataFrame,
    column: Hashable,
    drop: bool = False,
    **kwargs,
) -> gpd.GeoDataFrame:
    """
    Geocode a string type column from a DataFrame and get a GeoDataFrame of the
    resulting points.

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

    Raises
    ------
    ModuleNotFoundError
        If don't have module named 'geopy'.

    See Also
    --------
    geopandas.tools.geocode
    dtoolkit.geoaccessor.series.geocode

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd
    >>> df = pd.DataFrame(
    ...     {
    ...         "name": [
    ...             "boston, ma",
    ...             "1600 pennsylvania ave. washington, dc",
    ...         ],
    ...     }
    ... )
    >>> df
                                        name
    0                             boston, ma
    1  1600 pennsylvania ave. washington, dc
    >>> df.geocode("name", drop=True)
                        geometry                                            address
    0  POINT (-71.06051 42.35543)               Boston, Massachusetts, United States
    1  POINT (-77.03655 38.89770)  White House, 1600, Pennsylvania Avenue Northwe...
    """

    return pd.concat(
        (
            df.drop_or_not(drop=drop, columns=column),
            gpd.tools.geocode(df[column], **kwargs),
        ),
        axis=1,
    )
