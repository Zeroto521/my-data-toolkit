.. _transformer:

===========
Transformer
===========
.. currentmodule:: dtoolkit.transformer


Base Transformer
----------------

Base transformer class for all transformers.

.. autosummary::
    :toctree: api/

    Transformer
    MethodTF
    DataFrameTF
    NumpyTF
    methodtf_factory


Sklearn Transformer
-------------------
.. autosummary::
    :toctree: api/

    OneHotEncoder
    MinMaxScaler
    FeatureUnion
    make_union


Pandas Transformer
------------------

The parameters of transformer (``args``, ``kwargs``) are the same to
corresponding to relative :class:`pandas.DataFrame`'s method.

.. autosummary::
    :toctree: api/

    AssignTF
    AppendTF
    DropTF
    EvalTF
    FilterInTF
    FillnaTF
    GetTF
    QueryTF
    ReplaceTF
    SelectDtypesTF


Numpy Transformer
-----------------

The parameters of transformer (``args``, ``kwargs``) are the same to
corresponding to relative :class:`numpy.ndarray`'s method.

.. autosummary::
    :toctree: api/

    RavelTF
