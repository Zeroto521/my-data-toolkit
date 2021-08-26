.. _transformer:

Transformer
===========
.. currentmodule:: dtoolkit.transformer


Base Transformer
----------------

Base transformer class for all transformers.

.. autosummary::
    :toctree: api/transformer/base

    Transformer
    MethodTF
    DataFrameTF
    NumpyTF


Sklearn Transformer
-------------------
.. autosummary::
    :toctree: api/transformer/sklearn

    OneHotEncoder
    MinMaxScaler
    FeatureUnion
    make_union


Pandas Transformer
------------------

The parameters of transformer (``args``, ``kwargs``) are the same to 
corresponding to relative :class:`pandas.DataFrame`'s method.

.. autosummary::
    :toctree: api/transformer/pandas

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
    :toctree: api/transformer/numpy

    RavelTF
