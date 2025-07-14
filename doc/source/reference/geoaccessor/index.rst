==============
Index Accessor
==============
.. currentmodule:: dtoolkit.geoaccessor.index


H3 accessor
-----------

``Index.h3`` can be used to access the values of the Index(string) or Index(int64)
and apply several methods to it. These can be accessed like ``Index.h3.<function/property>``.

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
