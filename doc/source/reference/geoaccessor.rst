===========
GeoAccessor
===========

GeoSeries Accessor
------------------
.. currentmodule:: dtoolkit.geoaccessor.geoseries
.. autosummary::
    :toctree: api/

    count_coordinates
    geobuffer
    get_coordinates
    utm_crs


GeoDataFrame Accessor
---------------------
.. currentmodule:: dtoolkit.geoaccessor.geodataframe
.. autosummary::
    :toctree: api/

    count_coordinates
    geobuffer
    get_coordinates
    utm_crs


Series Accessor (to GeoPandas)
---------------
.. currentmodule:: dtoolkit.geoaccessor.series
.. autosummary::
    :toctree: api/

    to_geocode


DataFrame Accessor (to GeoPandas)
---------------------------------
.. currentmodule:: dtoolkit.geoaccessor.dataframe
.. autosummary::
    :toctree: api/

    from_wkt
    from_xy
    to_geocode
    to_geoframe


GeoPandas Base Accessor
-----------------------
.. currentmodule:: dtoolkit.geoaccessor
.. autosummary::
    :toctree: api/

    register_geoseries_accessor
    register_geodataframe_accessor


GeoPandas Method Register
-------------------------
.. currentmodule:: dtoolkit.geoaccessor
.. autosummary::
    :toctree: api/

    register_geoseries_method
    register_geodataframe_method
