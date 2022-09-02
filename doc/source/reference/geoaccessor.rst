===========
GeoAccessor
===========

GeoSeries Accessor
------------------
.. currentmodule:: dtoolkit.geoaccessor.geoseries
.. autosummary::
    :toctree: api/

    bd09_to_gcj02
    count_coordinates
    drop_duplicates_geometry
    duplicated_geometry
    duplicated_geometry_groups
    geoarea
    geobuffer
    get_coordinates
    has_hole
    hole_counts
    reverse_geocode
    toposimplify


GeoDataFrame Accessor
---------------------
.. currentmodule:: dtoolkit.geoaccessor.geodataframe
.. autosummary::
    :toctree: api/

    bd09_to_gcj02
    count_coordinates
    drop_duplicates_geometry
    drop_geometry
    duplicated_geometry
    duplicated_geometry_groups
    geoarea
    geobuffer
    get_coordinates
    has_hole
    hole_counts
    reverse_geocode
    toposimplify


Series Accessor (to GeoPandas)
------------------------------
.. currentmodule:: dtoolkit.geoaccessor.series
.. autosummary::
    :toctree: api/

    from_wkb
    from_wkt
    geocode
    to_geoframe
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
