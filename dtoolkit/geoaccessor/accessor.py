import geopandas as gpd
from pandas.core.accessor import _register_accessor
from pandas.util._decorators import doc


@doc(klass=":class:`~geopandas.GeoSeries`")
def register_geoseries_accessor(name: str):
    """
    Register a custom accessor on {klass} objects.

    This is a temparatory solution to hook method into
    :class:`~geopandas.GeoSeries` or :class:`~geopandas.GeoDataFrame`.
    If `geopandas#1952`_ done, it would be removed from
    :mod:`dtoolkit.geoaccessor`.

    .. _geopandas#1952: https://github.com/geopandas/geopandas/pull/1952

    Parameters
    ----------
    name : str
        Name under which the accessor should be registered. A warning is issued
        if this name conflicts with a preexisting attribute.

    Returns
    -------
    callable
        A class decorator.

    See Also
    --------
    register_geoseries_accessor
    register_geodataframe_accessor
    dtoolkit.geoaccessor.register_geoseries_method
    dtoolkit.geoaccessor.register_geodataframe_method

    Notes
    -----
    When accessed, your accessor will be initialized with the geopandas object
    the user is interacting with. So the signature must be::

        def __init__(self, geopandas_object):  # noqa: E999
            ...

    For consistency with geopandas methods, you should raise an
    ``AttributeError`` if the data passed to your accessor has an incorrect
    dtype.

    >>> import geopandas as gpd
    >>> gpd.GeoSeries().dt
    Traceback (most recent call last):
    ...
    AttributeError: Can only use .dt accessor with datetimelike values

    Examples
    --------
    In your library code::

        from pygeos import count_coordinates, from_shapely

        @register_geodataframe_accessor("coords")
        @register_geoseries_accessor("coords")
        class CoordinateAccessor:
            def __init__(self, gpd_obj):
                self._obj = gpd_obj
                self.geometry = gpd_obj.geometry

            @property
            def count_coordinates(self):
                # Counts the number of coordinate pairs in geometry

                foo = lambda x: count_coordinates(from_shapely(x))
                return self.geometry.apply(foo)

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

        In [4]: s.coords.count_coordinates
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

        In [6]: d.coords.count_coordinates
        Out[6]:
        0    1
        1    1
        2    0
        Name: geometry, dtype: int64
    """

    return _register_accessor(name, gpd.GeoSeries)


@doc(register_geoseries_accessor, klass=":class:`~geopandas.GeoDataFrame`")
def register_geodataframe_accessor(name: str):

    return _register_accessor(name, gpd.GeoDataFrame)
