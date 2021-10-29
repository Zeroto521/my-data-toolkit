from pandas.util._decorators import doc

from dtoolkit.accessor.register import register_method_factory
from dtoolkit.geoaccessor.accessor import register_geodataframe_accessor
from dtoolkit.geoaccessor.accessor import register_geoseries_accessor


@register_method_factory
@doc(klass=":class:`geopandas.GeoSeries`")
def register_geoseries_method(method):
    """
    {klass} register accessor for human.

    Write method normally, use method naturally.

    See Also
    --------
    dtoolkit.geoaccessor.accessor.register_geoseries_accessor
    dtoolkit.geoaccessor.accessor.register_geodataframe_accessor
    dtoolkit.geoaccessor.register.register_geoseries_method
    dtoolkit.geoaccessor.register.register_geodataframe_method

    Examples
    --------
    In your library code::

        import geopandas as gpd

        from pygeos import count_coordinates, from_shapely

        @register_geoseries_method
        def count_coord(s: gpd.GeoSeries):
            # Counts the number of coordinate pairs in geometry

            func = lambda x: count_coordinates(from_shapely(x))
            return s.apply(func)

    Back in an interactive IPython session:

        .. code-block:: ipython

            In [1]: import geopandas as gpd

            In [2]: s = gpd.GeoSeries.from_wkt(["POINT (1 1)", None])

            In [3]: s.count_coord()
            Out[3]:
            0    1
            1    0
            dtype: int64
    """
    return register_geoseries_accessor(method)


@register_method_factory
@doc(register_geoseries_method, klass=":class:`geopandas.GeoDataFrame`")
def register_geodataframe_method(method):
    return register_geodataframe_accessor(method)
