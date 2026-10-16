import geopandas as gpd
import pandas as pd

from dtoolkit.geoaccessor.geoseries.geoazimuth import _azimuth
from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
def geoazimuth_matrix(
    s: gpd.GeoSeries,
    /,
    other: gpd.GeoSeries | gpd.GeoDataFrame | None = None,
) -> pd.DataFrame:
    """
    Returns a ``DataFrame`` containing the great-circle azimuth matrix between
    ``s`` and ``other``.

    Azimuth is measured clockwise from north, in the range ``[0, 360)``.

    .. math::

        \\theta = \\texttt{atan2}(
            \\sin(\\Delta\\lambda) \\cdot \\cos(\\varphi_2), \\\\
            \\cos(\\varphi_1) \\cdot \\sin(\\varphi_2)
            - \\sin(\\varphi_1) \\cdot \\cos(\\varphi_2) \\cdot \\cos(\\Delta\\lambda)
        )

    Parameters
    ----------
    other : GeoSeries or GeoDataFrame, default None
        If None, uses ``other=s``.

    Returns
    -------
    DataFrame
        - The index and columns are the same as the index of ``s`` and ``other``.
        - The values are azimuth (degrees) in range ``[0, 360)``.

    Raises
    ------
    ValueError
        If the CRS is not ``EPSG:4326``.

    TypeError
        If the other is not a GeoSeries, GeoDataFrame, or None type.

    See Also
    --------
    dtoolkit.geoaccessor.geoseries.geoazimuth
    dtoolkit.geoaccessor.geoseries.geoazimuth_matrix
    dtoolkit.geoaccessor.geodataframe.geoazimuth
    dtoolkit.geoaccessor.geodataframe.geoazimuth_matrix
    dtoolkit.geoaccessor.geoseries.geodistance_matrix

    Notes
    -----
    - Currently, only supports Point geometry.
    - ``0°`` indicates due north, ``90°`` due east, ``180°`` due south,
      ``270°`` due west.

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd
    >>> df = (
    ...     pd.DataFrame({"x": [116.4, 121.5], "y": [39.9, 31.2]})
    ...     .from_xy("x", "y", crs=4326)
    ... )
    >>> other = (
    ...     pd.DataFrame({"x": [120, 110], "y": [30, 40]})
    ...     .from_xy("x", "y", crs=4326)
    ... )
    >>> df.geoazimuth_matrix(other)
                0           1
    0  162.343098  273.222468
    1  227.478645  316.502506

    Self-azimuth matrix:

    >>> df.geoazimuth_matrix()
                0           1
    0    0.000000  152.977873
    1  335.952943    0.000000
    """
    if other is None:
        other = s.copy()

    if not isinstance(other, gpd.base.GeoPandasBase):
        raise TypeError(f"Unknown type: {type(other).__name__!r}.")
    if s.crs != 4326:
        raise ValueError(f"Only support 'EPSG:4326' CRS, but got {s.crs!r}.")
    if other.crs != 4326:
        raise ValueError(f"Only support 'EPSG:4326' CRS, but got {other.crs!r}.")

    coords1 = s.get_coordinates().loc[:, ["x", "y"]].to_numpy()  # (n, 2) [lon, lat]
    coords2 = other.get_coordinates().loc[:, ["x", "y"]].to_numpy()  # (m, 2)

    x1, y1 = coords1[:, 0][:, None], coords1[:, 1][:, None]  # (n, 1)
    x2, y2 = coords2[:, 0][None, :], coords2[:, 1][None, :]  # (1, m)
    return pd.DataFrame(_azimuth(x1, y1, x2, y2), index=s.index, columns=other.index)
