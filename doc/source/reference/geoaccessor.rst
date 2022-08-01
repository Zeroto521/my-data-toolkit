===========
GeoAccessor
===========

GeoSeries Accessor
------------------
.. currentmodule:: dtoolkit.geoaccessor.geoseries
.. autosummary::
    :toctree: api/

    count_coordinates
    duplicated_geometry
    duplicated_geometry_groups
    geobuffer
    get_coordinates
    reverse_geocode
    utm_crs


GeoDataFrame Accessor
---------------------
.. currentmodule:: dtoolkit.geoaccessor.geodataframe
.. autosummary::
    :toctree: api/

    count_coordinates
    drop_geometry
    duplicated_geometry_groups
    geobuffer
    get_coordinates
    reverse_geocode
    utm_crs


Series Accessor (to GeoPandas)
------------------------------
.. currentmodule:: dtoolkit.geoaccessor.series
.. autosummary::
    :toctree: api/

    from_wkb
    from_wkt
    geocode
    to_geoseries


DataFrame Accessor (to GeoPandas)
---------------------------------
.. currentmodule:: dtoolkit.geoaccessor.dataframe
.. autosummary::
    :toctree: api/

    from_wkb
    from_wkt
    from_xy
    geocode
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
