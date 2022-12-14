import geopandas as gpd
import pandas as pd

from dtoolkit.geoaccessor.register import register_geodataframe_method


@register_geodataframe_method
def drop_geometry(df: gpd.GeoDataFrame, /) -> pd.DataFrame:
    """
    Drop the activate geometry column from the :class:`~geopandas.GeoDataFrame`
    to return a normal :class:`~pandas.DataFrame`.

    Returns
    -------
    DataFrame
        Dropped active geometry column.

    See Also
    --------
    geopandas.GeoDataFrame.rename_geometry
    geopandas.GeoDataFrame.set_geometry

    Notes
    -----
    If you want to set another column as the active geometry, please use
    :meth:`~geopandas.GeoDataFrame.set_geometry` instead.

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd
    >>> df = pd.DataFrame(
    ...     {
    ...         "x": [122, 100],
    ...         "y": [55, 1],
    ...         "name": ["a", "b"],
    ...     },
    ... ).from_xy("x", "y", crs=4326)
    >>> df
         x   y name                    geometry
    0  122  55    a  POINT (122.00000 55.00000)
    1  100   1    b   POINT (100.00000 1.00000)
    >>> df.drop_geometry()
         x   y name
    0  122  55    a
    1  100   1    b

    Drop customed geometry column.

    >>> df_new = df.rename_geometry("geom")
    >>> df_new
         x   y name                        geom
    0  122  55    a  POINT (122.00000 55.00000)
    1  100   1    b   POINT (100.00000 1.00000)
    >>> df_new.drop_geometry()
         x   y name
    0  122  55    a
    1  100   1    b
    """

    return df.drop(columns=df.geometry.name)
