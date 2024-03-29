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

``Series.h3`` can be used to access the index of string or int64
and apply several methods to it. These can be accessed like ``Series.h3.<function/property>``.

.. autosummary::
    :toctree: ../api/

    is_h3
    H3
    H3.area
    H3.resolution
    H3.is_valid
    H3.is_pentagon
    H3.is_res_class_iii
    H3.to_int
    H3.to_str
    H3.to_center_child
    H3.to_children
    H3.to_parent
    H3.to_points
    H3.to_polygons
