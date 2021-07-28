from __future__ import annotations

import numpy as np
import pandas as pd
from more_itertools import flatten
from pandas.util._decorators import doc
from sklearn.base import TransformerMixin
from sklearn.pipeline import _name_estimators
from sklearn.pipeline import FeatureUnion as SKFeatureUnion
from sklearn.preprocessing import MinMaxScaler as SKMinMaxScaler
from sklearn.preprocessing import OneHotEncoder as SKOneHotEncoder

from ._checking import check_dataframe_type
from ._checking import istype
from ._typing import PandasTypeList
from .accessor import ColumnAccessor  # noqa
from .accessor import FilterInAccessor  # noqa


__all__ = [
    "FeatureUnion",
    "make_union",
    "MinMaxScaler",
    "OneHotEncoder",
    "AssignTF",
    "AppendTF",
    "DropTF",
    "EvalTF",
    "FillnaTF",
    "FilterInTF",
    "FilterTF",
    "GetTF",
    "QueryTF",
    "ReplaceTF",
    "SelectDtypesTF",
    "RavelTF",
]


class Transformer(TransformerMixin):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def operate(self, X, *_, **__):
        return X

    def validate(self, *_, **__):
        ...

    def fit(self, *_):
        return self

    def transform(self, X, *_):
        self.validate(X)

        return self.operate(X, *self.args, **self.kwargs)

    def fit_transform(self, X, *_):
        return self.fit().transform(X)

    def inverse_transform(self, X, *_):
        return X


#
# Sklearn's operation
#


class FeatureUnion(SKFeatureUnion):
    """
    Concatenates results of multiple transformer objects.

    This estimator applies a list of transformer objects in parallel to the
    input data, then concatenates the results. This is useful to combine
    several feature extraction mechanisms into a single transformer.

    Parameters of the transformers may be set using its name and the parameter
    name separated by a '__'. A transformer may be replaced entirely by
    setting the parameter with its name to another transformer,
    or removed by setting to 'drop'.

    Parameters
    ----------
    transformer_list : list of (string, transformer) tuples
        List of transformer objects to be applied to the data. The first
        half of each tuple is the name of the transformer. The tranformer can
        be 'drop' for it to be ignored.

    n_jobs : int, default=None
        Number of jobs to run in parallel.
        ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context.
        ``-1`` means using all processors. See :term:`Glossary <n_jobs>`
        for more details.

    transformer_weights : dict, default=None
        Multiplicative weights for features per transformer.
        Keys are transformer names, values the weights.
        Raises ValueError if key not present in ``transformer_list``.

    verbose : bool, default=False
        If True, the time elapsed while fitting each transformer will be
        printed as it is completed.

    See Also
    --------
    make_union : Convenience function for simplified feature union
        construction.

    Notes
    -----
    Different to :obj:`sklearn.pipeline.FeatureUnion`.
    This would let pandas in and pandas out.

    Examples
    --------
    >>> from dtoolkit.transformer import FeatureUnion
    >>> from sklearn.decomposition import PCA, TruncatedSVD
    >>> union = FeatureUnion([("pca", PCA(n_components=1)),
    ...                       ("svd", TruncatedSVD(n_components=2))])
    >>> X = [[0., 1., 3], [2., 2., 5]]
    >>> union.fit_transform(X)
    array([[ 1.5       ,  3.0...,  0.8...],
           [-1.5       ,  5.7..., -0.4...]])
    """

    def _hstack(self, Xs):
        if all(istype(i, PandasTypeList) for i in Xs):
            Xs = (i.reset_index(drop=True) for i in Xs)
            return pd.concat(Xs, axis=1)

        return super()._hstack(Xs)


# make_union function ported with modifications from scikit-learn
# https://github.com/scikit-learn/scikit-learn/blob/master/sklearn/pipeline.py


def make_union(
    *transformers: list,
    n_jobs: int | None = None,
    verbose: bool = False,
) -> FeatureUnion:
    """
    Construct a FeatureUnion from the given transformers.

    This is a shorthand for the FeatureUnion constructor; it does not require,
    and does not permit, naming the transformers. Instead, they will be given
    names automatically based on their types. It also does not allow weighting.

    Parameters
    ----------
    *transformers : list of estimators

    n_jobs : int, default=None
        Number of jobs to run in parallel.
        ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context.
        ``-1`` means using all processors. See :term:`Glossary <n_jobs>`
        for more details.

    verbose : bool, default=False
        If True, the time elapsed while fitting each transformer will be
        printed as it is completed.

    Returns
    -------
    f : FeatureUnion

    See Also
    --------
    FeatureUnion : Class for concatenating the results of multiple transformer
        objects.

    Notes
    -----
    Different to :obj:`sklearn.pipeline.make_union`.
    This would let pandas in and pandas out.

    Examples
    --------
    >>> from sklearn.decomposition import PCA, TruncatedSVD
    >>> from dtoolkit.transformer import make_union
    >>> make_union(PCA(), TruncatedSVD())
     FeatureUnion(transformer_list=[('pca', PCA()),
                                   ('truncatedsvd', TruncatedSVD())])
    """
    return FeatureUnion(
        _name_estimators(transformers),
        n_jobs=n_jobs,
        verbose=verbose,
    )


def _change_data_to_df(
    data: np.ndarray,
    df: pd.DataFrame | np.ndarray,
) -> pd.DataFrame | np.ndarray:
    if isinstance(df, pd.DataFrame):
        return pd.DataFrame(data, columns=df.columns, index=df.index)

    return data


@doc(SKMinMaxScaler)
class MinMaxScaler(SKMinMaxScaler):
    def transform(self, X, *_):
        X_new = super().transform(X, *_)

        return _change_data_to_df(X_new, X)

    def inverse_transform(self, X, *_):
        X_new = super().inverse_transform(X, *_)

        return _change_data_to_df(X_new, X)


@doc(SKOneHotEncoder)
class OneHotEncoder(SKOneHotEncoder):
    def __init__(
        self,
        categories="auto",
        drop=None,
        sparse=False,
        dtype=np.float64,
        handle_unknown="error",
    ):
        super().__init__(
            categories=categories,
            drop=drop,
            sparse=sparse,
            dtype=dtype,
            handle_unknown=handle_unknown,
        )

    def transform(self, X, *_):
        X_new = super().transform(X, *_)

        if self.sparse is False:
            categories = flatten(self.categories_)
            return pd.DataFrame(X_new, columns=categories)

        return X_new


#
# Pandas's operation
#


class DataFrameTF(Transformer):
    def validate(self, *args, **kwargs):
        return check_dataframe_type(*args, **kwargs)


class AssignTF(Transformer):
    def operate(self, *args, **kwargs):
        return pd.DataFrame.assign(*args, **kwargs)


class AppendTF(DataFrameTF):
    def operate(self, *args, **kwargs):
        return pd.DataFrame.append(*args, **kwargs)


class DropTF(DataFrameTF):
    def operate(self, *args, **kwargs):
        return pd.DataFrame.drop(*args, **kwargs)


class EvalTF(DataFrameTF):
    def operate(self, *args, **kwargs):
        return pd.DataFrame.eval(*args, **kwargs)


class FillnaTF(DataFrameTF):
    def operate(self, *args, **kwargs):
        return pd.DataFrame.fillna(*args, **kwargs)


class FilterInTF(DataFrameTF):
    def transform(self, X, *_):
        self.validate(X)

        return X.filterin(*self.args, **self.kwargs)


class FilterTF(DataFrameTF):
    def operate(self, *args, **kwargs):
        return pd.DataFrame.filter(*args, **kwargs)


class GetTF(Transformer):
    def operate(self, *args, **kwargs):
        return pd.DataFrame.get(*args, **kwargs)


class QueryTF(DataFrameTF):
    def operate(self, *args, **kwargs):
        return pd.DataFrame.query(*args, **kwargs)


class ReplaceTF(DataFrameTF):
    def operate(self, *args, **kwargs):
        return pd.DataFrame.replace(*args, **kwargs)


class SelectDtypesTF(DataFrameTF):
    def operate(self, *args, **kwargs):
        return pd.DataFrame.select_dtypes(*args, **kwargs)


#
# numpy's operation
#


class RavelTF(Transformer):
    def operate(self, *args, **kwargs):
        return np.ravel(*args, **kwargs)
