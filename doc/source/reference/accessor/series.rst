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
    to_zh
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
    textdistance
    textdistance_matrix
    top_n


Reindexing / Selection
----------------------
.. autosummary::
    :toctree: ../api/

    filter_in
    invert_or_not
    query
    set_unique_index


Missing values
--------------
.. autosummary::
    :toctree: ../api/

    drop_inf
    drop_not_duplicates
    dropna_index


Reshaping / Transposing
-----------------------
.. autosummary::
    :toctree: ../api/

    expand
