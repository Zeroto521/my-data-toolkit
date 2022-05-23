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


Pipeline
-------------------

.. deprecated:: 0.0.17
    The :mod:`dtoolkit.transformer.pipeline` package will be moved into
    :mod:`dtoolkit.pipeline` in 0.0.17. (Warning added DToolKit 0.0.16)

.. autosummary::
    :toctree: api/

    Pipeline
    make_pipeline
    FeatureUnion
    make_union


Sklearn Transformer
-------------------
.. autosummary::
    :toctree: api/

    OneHotEncoder


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
