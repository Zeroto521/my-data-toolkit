==================
DataFrame Accessor
==================
.. currentmodule:: dtoolkit.geoaccessor.dataframe


Conversion
----------
.. autosummary::
    :toctree: ../api/

    from_xy
    from_wkt
    from_wkb
    to_geoframe
    to_line


Address handling
----------------
.. autosummary::
    :toctree: ../api/

    geocode


H3 accessor
-----------

``DataFrame.h3`` can be used to access the index of string or int64
and apply several methods to it. These can be accessed like ``DataFrame.h3.<function/property>``.

.. autosummary::
    :toctree: ../api/

    is_h3
    H3
    H3.area
    H3.resolution
    H3.is_valid
    H3.is_pentagon
    H3.is_res_class_III
    H3.to_int
    H3.to_str
    H3.to_center_child
    H3.to_children
    H3.to_parent
    H3.to_points
    H3.to_polygons
