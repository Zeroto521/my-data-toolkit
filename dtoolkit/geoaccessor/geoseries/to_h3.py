import geopandas as gpd
import pandas as pd

from dtoolkit.accessor.series import getattr as s_getattr
from dtoolkit.accessor.series import len as s_len
from dtoolkit.geoaccessor.geoseries.xy import xy
from dtoolkit.geoaccessor.register import register_geoseries_method
from dtoolkit.geoaccessor.series import to_geoframe


@register_geoseries_method
def to_h3(
    s: gpd.GeoSeries,
    /,
    resolution: int,
    int_dtype: bool = True,
) -> gpd.GeoSeries:
    """
    Convert Point or Polygon to H3 cell index.

    Parameters
    ----------
    resolution : int
        H3 resolution.

    int_dtype : bool, default True
        If True, use ``h3.api.numpy_int`` else use ``h3.api.basic_str``.

    Returns
    -------
    GeoSeries
        With H3 cell as the its index.

    Raises
    ------
    ModuleNotFoundError
        If don't have module named 'h3'.

    TypeError
        If the geometry type is not Point or Polygon.

    ValueError
        If the CRS is not WGS84 or EPSG:4326.

    See Also
    --------
    h3.latlon_to_h3
    h3.polygon_to_cells
    dtoolkit.geoaccessor.series.H3
    dtoolkit.geoaccessor.geodataframe.to_h3

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd

    Points to h3 indexes.

    >>> s = pd.Series(
    ...     [
    ...         "POINT (122 55)",
    ...         "POINT (100 1)",
    ...     ],
    ... ).from_wkt(crs=4326, drop=True)
    >>> s
    0    POINT (122.00000 55.00000)
    1     POINT (100.00000 1.00000)
    dtype: geometry
    >>> s.to_h3(8)
    0    612845052823076863
    1    614269156845420543
    dtype: int64

    Keep the geometry column.

    >>> s.to_h3(8, drop=False)
                         h3                    geometry
    0    612845052823076863  POINT (122.00000 55.00000)
    1    614269156845420543   POINT (100.00000 1.00000)

    Polygons to h3 indexes.

    >>> s = pd.Series(
    ...     [
    ...         "POLYGON ((1 0, 1 1, 0 1, 0 0, 1 0))",
    ...         "POLYGON ((2 1, 2 2, 1 2, 1 1, 2 1))",
    ...     ],
    ... ).from_wkt(crs=4326, drop=True)
    >>> s
    0    POLYGON ((1.00000 0.00000, 1.00000 1.00000, 0....
    1    POLYGON ((2.00000 1.00000, 2.00000 2.00000, 1....
    dtype: geometry
    >>> s.to_h3(4)
    0    596538839648960511
    0    596538693620072447
    0    596538685030137855
    0    596538848238895103
    0    596537920525959167
    0    596538813879156735
    0    596538856828829695
    0    596538805289222143
    1    596538229763604479
    1    596537946295762943
    1    596540780974178303
    1    596540729434570751
    1    596540772384243711
    1    596538212583735295
    1    596540763794309119
    1    596537954885697535
    1    596540746614439935
    1    596538195403866111
    1    596541030082281471
    dtype: object

    Also support str (hexadecimal) format.

    >>> s = pd.Series(
    ...     [
    ...         "POINT (122 55)",
    ...         "POINT (100 1)",
    ...     ],
    ... ).from_wkt(crs=4326, drop=True)
    >>> s
    0    POINT (122.00000 55.00000)
    1     POINT (100.00000 1.00000)
    dtype: geometry
    >>> s.to_h3(8, int_dtype=False)
    0    88143541bdfffff
    1    886528b2a3fffff
    dtype: object
    """

    # TODO: Advices for h3-pandas
    # 1. use `import h3.api.numpy_int as h3` instead of `import h3`
    # 2. compat with h3-py 4
    # 3. requires crs is 4326
    # 4. consider h3-py as the accessor of Series
    # 6. Speed up creating points / polygons via pygeos

    if s.crs != 4326:
        raise ValueError(f"Only support 'EPSG:4326' CRS, but got {s.crs!r}.")

    if all(s.geom_type == "Point"):
        h3 = points_to_h3(s, resolution=resolution, int_dtype=int_dtype)
    elif all(s.geom_type == "Polygon"):
        h3_list = polygons_to_h3(s, resolution=resolution, int_dtype=int_dtype)
        h3 = h3_list.explode()
        s = s.repeat(s_len(h3_list))
    else:
        raise TypeError("Only support 'Point' or 'Polygon' geometry type.")

    return h3 if drop else to_geoframe(h3.rename(name or s.name), geometry=s)


def points_to_h3(s: gpd.GeoSeries, /, resolution: int, int_dtype: bool) -> pd.Series:
    # TODO: Use `latlon_to_h3` instead of `geo_to_h3`
    # While h3-py release 4, `latlon_to_h3` is not available.
    method = method_from_h3("geo_to_h3", int_dtype=int_dtype)

    return xy(s, reverse=True, frame=False, name=None).apply(
        lambda yx: method(*yx, resolution),
    )


def polygons_to_h3(s: gpd.GeoSeries, /, resolution: int, int_dtype: bool) -> pd.Series:
    # TODO: Use `polygon_to_cells` instead of `geo_to_h3`
    # While h3-py release 4, `polygon_to_cells` is not available.

    # If `geo_json_conformant` is True, the coordinate could be (lon, lat).
    return s_getattr(s, "__geo_interface__").apply(
        method_from_h3("polyfill", int_dtype=int_dtype),
        res=resolution,
        geo_json_conformant=True,
    )


def method_from_h3(method: str, int_dtype: bool = True) -> callable:
    if int_dtype:
        import h3.api.numpy_int as h3
    else:
        import h3.api.basic_str as h3

    return getattr(h3, method)
