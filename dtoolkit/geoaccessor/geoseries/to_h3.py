import geopandas as gpd
from pandas._libs.reshape import explode
from pandas.util._decorators import doc

from dtoolkit.accessor.series import getattr as s_getattr
from dtoolkit.geoaccessor.geoseries.xy import xy
from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
@doc(klass="GeoSeries")
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
    {klass}
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
    dtoolkit.geoaccessor.dataframe.H3
    dtoolkit.geoaccessor.geoseries.to_h3
    dtoolkit.geoaccessor.geodataframe.to_h3

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd

    Points to h3 indexes.

    >>> df = pd.DataFrame({{"x": [122, 100], "y": [55, 1]}}).from_xy('x', 'y', crs=4326)
    >>> df
         x   y                    geometry
    0  122  55  POINT (122.00000 55.00000)
    1  100   1   POINT (100.00000 1.00000)
    >>> df.to_h3(8)
                          x   y                    geometry
    612845052823076863  122  55  POINT (122.00000 55.00000)
    614269156845420543  100   1   POINT (100.00000 1.00000)

    Polygons to h3 indexes.

    >>> df = pd.DataFrame(
    ...     {{
    ...         "label": ["a", "b"],
    ...         "wkt": [
    ...             "POLYGON ((1 0, 1 1, 0 1, 0 0, 1 0))",
    ...             "POLYGON ((2 1, 2 2, 1 2, 1 1, 2 1))",
    ...         ],
    ...     }},
    ... ).from_wkt("wkt", crs=4326).drop(columns="wkt")
    >>> df
      label                                           geometry
    0     a  POLYGON ((1.00000 0.00000, 1.00000 1.00000, 0....
    1     b  POLYGON ((2.00000 1.00000, 2.00000 2.00000, 1....
    >>> df.to_h3(4)
                       label                                           geometry
    596538839648960511     a  POLYGON ((1.00000 0.00000, 1.00000 1.00000, 0....
    596538693620072447     a  POLYGON ((1.00000 0.00000, 1.00000 1.00000, 0....
    596538685030137855     a  POLYGON ((1.00000 0.00000, 1.00000 1.00000, 0....
    596538848238895103     a  POLYGON ((1.00000 0.00000, 1.00000 1.00000, 0....
    596537920525959167     a  POLYGON ((1.00000 0.00000, 1.00000 1.00000, 0....
    596538813879156735     a  POLYGON ((1.00000 0.00000, 1.00000 1.00000, 0....
    596538856828829695     a  POLYGON ((1.00000 0.00000, 1.00000 1.00000, 0....
    596538805289222143     a  POLYGON ((1.00000 0.00000, 1.00000 1.00000, 0....
    596538229763604479     b  POLYGON ((2.00000 1.00000, 2.00000 2.00000, 1....
    596537946295762943     b  POLYGON ((2.00000 1.00000, 2.00000 2.00000, 1....
    596540780974178303     b  POLYGON ((2.00000 1.00000, 2.00000 2.00000, 1....
    596540729434570751     b  POLYGON ((2.00000 1.00000, 2.00000 2.00000, 1....
    596540772384243711     b  POLYGON ((2.00000 1.00000, 2.00000 2.00000, 1....
    596538212583735295     b  POLYGON ((2.00000 1.00000, 2.00000 2.00000, 1....
    596540763794309119     b  POLYGON ((2.00000 1.00000, 2.00000 2.00000, 1....
    596537954885697535     b  POLYGON ((2.00000 1.00000, 2.00000 2.00000, 1....
    596540746614439935     b  POLYGON ((2.00000 1.00000, 2.00000 2.00000, 1....
    596538195403866111     b  POLYGON ((2.00000 1.00000, 2.00000 2.00000, 1....
    596541030082281471     b  POLYGON ((2.00000 1.00000, 2.00000 2.00000, 1....

    Also support str (hexadecimal) format.

    >>> df = pd.DataFrame({{"x": [122, 100], "y": [55, 1]}}).from_xy('x', 'y', crs=4326)
    >>> df
         x   y                    geometry
    0  122  55  POINT (122.00000 55.00000)
    1  100   1   POINT (100.00000 1.00000)
    >>> df.to_h3(8, int_dtype=False)
                       x   y                    geometry
    88143541bdfffff  122  55  POINT (122.00000 55.00000)
    886528b2a3fffff  100   1   POINT (100.00000 1.00000)
    """

    # TODO: Advices for h3-pandas
    # 1. use `import h3.api.numpy_int as h3` instead of `import h3`
    # 2. compat with h3-py 4
    # 3. requires crs is 4326
    # 4. consider h3-py as the accessor of Series
    # 6. Speed up creating points / polygons via shapely 2.x

    if int_dtype:
        import h3.api.numpy_int as h3
    else:
        import h3.api.basic_str as h3

    if s.crs != 4326:
        raise ValueError(f"Only support 'EPSG:4326' CRS, but got {s.crs!r}.")

    if all(s.geom_type == "Point"):
        # TODO: Use `latlon_to_h3` instead of `geo_to_h3`
        # While h3-py release 4, `latlon_to_h3` is not available.
        return s.set_axis(
            xy(s.geometry, reverse=True, frame=False, name=None)
            .apply(lambda yx: getattr(h3, "geo_to_h3")(*yx, resolution))
            .to_numpy(),
        )
    elif all(s.geom_type == "Polygon"):
        # TODO: Use `polygon_to_cells` instead of `geo_to_h3`
        # While h3-py release 4, `polygon_to_cells` is not available.
        # If `geo_json_conformant` is True, the coordinate could be (lon, lat).
        index, counts = explode(
            s_getattr(s.geometry, "__geo_interface__")
            .apply(getattr(h3, "polyfill"), res=resolution, geo_json_conformant=True)
            .to_numpy(),
        )
        return s.repeat(counts).set_axis(index)

    raise TypeError("Only support 'Point' or 'Polygon' geometry type.")
