=====================
GeoDataFrame Accessor
=====================
.. currentmodule:: dtoolkit.geoaccessor.geodataframe


General methods and attributes
------------------------------
.. autosummary::
    :toctree: ../api/

    count_coordinates
    geoarea
    geobuffer
    geodistance_matrix
    geodistance
    get_coordinates
    has_hole
    hole_counts
    toposimplify
    xy


Conversion
----------
.. autosummary::
    :toctree: ../api/

    to_h3


Projection handling
-------------------
.. autosummary::
    :toctree: ../api/

    cncrs_offset


Active geometry handling
------------------------
.. autosummary::
    :toctree: ../api/

    drop_duplicates_geometry
    drop_geometry
    duplicated_geometry
    duplicated_geometry_groups


Selection
---------
.. autosummary::
    :toctree: ../api/

    select_geom_type


Binary operator functions
-------------------------
.. autosummary::
    :toctree: ../api/

    filter_geometry


Address handling
----------------
.. autosummary::
    :toctree: ../api/

    reverse_geocode
