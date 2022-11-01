from pandas.util._decorators import doc

from dtoolkit.accessor.register import register_method_factory
from dtoolkit.geoaccessor.accessor import register_geodataframe_accessor
from dtoolkit.geoaccessor.accessor import register_geoseries_accessor


@register_method_factory
@doc(klass=":class:`~geopandas.GeoSeries`")
def register_geoseries_method(name: str = None):
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

        from __future__ import annotations

        import geopandas as gpd
        import pandas as pd


        @register_geodataframe_method("is_p")  # Support alias name also.
        @register_geoseries_method("is_p")  # Only receive positional-only argument.
        @register_geodataframe_method
        @register_geoseries_method  # Use accessor method `__name__` as the entrance.
        def is_point(s: gpd.GeoSeries | gpd.GeoDataFrame) -> pd.Series:
            # Return a boolean Series denoting whether each geometry is a point.

            return self._obj.geometry.geom_type == "Point"

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

        In [4]: s.is_point()
        Out[4]:
        0     True
        1     True
        2    False
        dtype: bool

        In [5]: d = s.to_frame("geometry")
        Out[5]:
                          geometry
        0  POINT (0.00000 0.00000)
        1  POINT (1.00000 1.00000)
        2                     None

        In [6]: d.is_point()
        Out[6]:
        0     True
        1     True
        2    False
        dtype: bool

        In [7]: s.is_p()
        Out[7]:
        0     True
        1     True
        2    False
        dtype: bool

        In [8]: d.is_p()
        Out[8]:
        0     True
        1     True
        2    False
        dtype: bool

    """
    return register_geoseries_accessor(name)


@register_method_factory
@doc(register_geoseries_method, klass=":class:`~geopandas.GeoDataFrame`")
def register_geodataframe_method(name: str = None):
    return register_geodataframe_accessor(name)
