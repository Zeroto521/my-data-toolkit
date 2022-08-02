========
Accessor
========


Index Accessor
---------------
.. currentmodule:: dtoolkit.accessor.index
.. autosummary::
    :toctree: api/

    to_set

Series Accessor
---------------
.. currentmodule:: dtoolkit.accessor.series
.. autosummary::
    :toctree: api/

    bin
    cols
    drop_inf
    error_report
    eval
    expand
    filter_in
    getattr
    groupby_index
    jenks_bin
    jenks_breaks
    len
    query
    swap_index_values
    to_set
    top_n
    values_to_dict


DataFrame Accessor
------------------
.. currentmodule:: dtoolkit.accessor.dataframe
.. autosummary::
    :toctree: api/

    boolean
    cols
    decompose
    drop_inf
    drop_or_not
    expand
    fillna_regression
    filter_in
    groupby_index
    repeat
    to_series
    top_n
    values_to_dict


Pandas Method Register
----------------------
.. currentmodule:: dtoolkit.accessor
.. autosummary::
    :toctree: api/

    register_method_factory
    register_dataframe_method
    register_series_method
    register_index_method
