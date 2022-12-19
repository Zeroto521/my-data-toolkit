===============
Series Accessor
===============
.. currentmodule:: dtoolkit.geoaccessor.series


Conversion
----------
.. autosummary::
    :toctree: ../api/

    from_wkt
    from_wkb
    to_geoseries
    to_geoframe


Address handling
----------------
.. autosummary::
    :toctree: ../api/

    geocode


H3 accessor
-----------

``Series.h3`` can be used to access the values of the Series(string) or Series(int64)
and apply several methods to it. These can be accessed like ``Series.h3.<function/property>``.

.. autosummary::
    :toctree: ../api/

    is_h3
    h3
    h3.area
    h3.resolution
    h3.is_valid
    h3.is_pentagon
    h3.is_res_class_iii
    h3.to_int
    h3.to_str
    h3.to_center_child
    h3.to_children
    h3.to_parent
    h3.to_points
    h3.to_polygons
