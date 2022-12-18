=====================
GeoDataFrame Accessor
=====================
.. currentmodule:: dtoolkit.geoaccessor.geodataframe


General methods and attributes
------------------------------
.. autosummary::
    :toctree: ../api/

    xy
    geoarea
    geodistance
    geodistance_matrix
    geobuffer
    get_coordinates
    count_coordinates
    has_hole
    hole_counts
    toposimplify


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

    drop_geometry
    drop_duplicates_geometry
    duplicated_geometry
    duplicated_geometry_groups


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
