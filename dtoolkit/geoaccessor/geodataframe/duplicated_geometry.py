from warnings import warn

import geopandas as gpd
import pandas as pd

from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
def duplicated_geometry(df: gpd.GeoDataFrame, /, **kwargs) -> pd.Series:
    return (
        df.geometry.to_frame()
        .pipe(set_unique_index, drop=True)
        .pipe(self_sjoin, **kwargs)
        .groupby_index()
        .geometry.count()
        .set_axis(df.index)
        .rename(None)
    )


def set_unique_index(df: pd.DataFrame, /, **kwargs) -> pd.DataFrame:
    """
    Set unique index via ``.reset_index`` if ``df.index`` isn't unique.

    Parameters
    ----------
    **kwargs
        See the documentation for :meth:`~pandas.DataFrame.set_index` for complete
        details on the keyword arguments.

    Returns
    -------
    DataFrame

    See Also
    --------
    pandas.DataFrame.reset_index
    """

    if not df.index.is_unique:
        warn(f"The 'Index' of {type(df)} is not unique.")
        return df.reset_index(**kwargs)

    return df


def self_sjoin(df: gpd.GeoDataFrame, /, **kwargs) -> gpd.GeoDataFrame:
    """
    Perform self-sjoin on a GeoDataFrame.

    Parameters
    ----------
    **kwargs
        See the documentation for :meth:`~geopandas.GeoDataFrame.sjoin` for complete
        details on the keyword arguments except ``left_df`` and ``right_df``.

    Returns
    -------
    GeoDataFrame

    See Also
    --------
    geopandas.GeoDataFrame.sjoin

    Notes
    -----
    ``left_df`` and ``right_df`` parameter are ``df`` and can't be overridden.
    """

    return gpd.sjoin(df, df, **kwargs)
