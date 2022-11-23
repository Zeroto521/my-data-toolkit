===============
Series Accessor
===============
.. currentmodule:: dtoolkit.accessor.series


General methods and attributes
------------------------------
.. autosummary::
    :toctree: ../api/

    cols
    len
    getattr


Conversion
----------
.. autosummary::
    :toctree: ../api/

    change_axis_type
    swap_index_values
    to_datetime
    to_set
    values_to_dict


Binary operator functions
-------------------------
.. autosummary::
    :toctree: ../api/

    equal


GroupBy
-------
.. autosummary::
    :toctree: ../api/

    groupby_index


Computations / Descriptive Stats
--------------------------------
.. autosummary::
    :toctree: ../api/

    bin
    jenks_bin
    jenks_breaks
    error_report
    eval
    top_n


Reindexing / Selection / Label manipulation
-------------------------------------------
.. autosummary::
    :toctree: ../api/

    duplicated_groups
    filter_in
    query
    set_unique_index


Missing values
--------------
.. autosummary::
    :toctree: ../api/

    drop_inf
    dropna_index


Reshaping / Transposing
-----------------------
.. autosummary::
    :toctree: ../api/

    expand
