==============================
Series Accessor (to GeoPandas)
==============================
.. currentmodule:: dtoolkit.geoaccessor.series


Conversion
----------
.. autosummary::
    :toctree: ../api/

    from_wkb
    from_wkt
    to_geoframe
    to_geoseries


Address handling
----------------
.. autosummary::
    :toctree: ../api/

    geocode


H3 (Hexagonal hierarchical geospatial indexing system)
------------------------------------------------------
.. autosummary::
    :toctree: ../api/

    is_h3
    H3
    H3.is_valid
    H3.is_pentagon
    H3.is_res_class_III
    H3.resolution
    H3.edge_length
    H3.area
    H3.to_str
    H3.to_int
    H3.to_points
    H3.to_polygons
    H3.to_parent
    H3.to_children
    H3.to_center_child
