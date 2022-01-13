from __future__ import annotations

from pandas.util._decorators import doc

from dtoolkit.accessor.register import register_method_factory
from dtoolkit.geoaccessor.accessor import register_geodataframe_accessor
from dtoolkit.geoaccessor.accessor import register_geoseries_accessor


@register_method_factory
@doc(klass=":class:`~geopandas.GeoSeries`")
def register_geoseries_method(name: str | None = None):
    """
    {klass} register accessor for human.

    Write method normally, use method naturally.

    Parameters
    ----------
    name : str, optional
        Use the ``method`` name as the default accessor entrance if ``name`` is None.

    See Also
    --------
    dtoolkit.geoaccessor.register_geoseries_accessor
    dtoolkit.geoaccessor.register_geodataframe_accessor
    register_geoseries_method
    register_geodataframe_method

    Examples
    --------
    In your library code::

        import geopandas as gpd

        from pygeos import count_coordinates, from_shapely

        @register_geodataframe_method(name="count_it")
        @register_geoseries_method(name="count_it")  # Support alias name also.
        @register_geodataframe_method
        @register_geoseries_method  # Use accessor method `__name__` as the entrance.
        def counts(s: gpd.GeoSeries):
            # Counts the number of coordinate pairs in geometry

            func = lambda x: count_coordinates(from_shapely(x))
            return s.geometry.apply(func)

    Back in an interactive IPython session:

    .. code-block:: ipython

        In [1]: import geopandas as gpd

        In [2]: s = gpd.GeoSeries.from_wkt(["POINT (0 0)", "POINT (1 1)", None])

        In [3]: s
        Out[3]:
        0    POINT (0.00000 0.00000)
        1    POINT (1.00000 1.00000)
        2                       None
        dtype: geometry

        In [4]: s.counts()
        Out[4]:
        0    1
        1    1
        2    0
        dtype: int64

        In [5]: d = s.to_frame("geometry")
        Out[5]:
                        geometry
        0  POINT (0.00000 0.00000)
        1  POINT (1.00000 1.00000)
        2                     None

        In [6]: d.counts()
        Out[6]:
        0    1
        1    1
        2    0
        Name: geometry, dtype: int64

        In [7]: s.count_it()
        Out[7]:
        0    1
        1    1
        2    0
        dtype: int64

        In [8]: d.count_it()
        Out[8]:
        0    1
        1    1
        2    0
        Name: geometry, dtype: int64

    """
    return register_geoseries_accessor(name)


@register_method_factory
@doc(register_geoseries_method, klass=":class:`~geopandas.GeoDataFrame`")
def register_geodataframe_method(name: str | None = None):
    return register_geodataframe_accessor(name)
