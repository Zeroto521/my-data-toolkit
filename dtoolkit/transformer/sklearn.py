from __future__ import annotations

from textwrap import dedent

import numpy as np
import pandas as pd
from more_itertools import flatten
from pandas.util._decorators import doc
from sklearn.pipeline import _name_estimators
from sklearn.pipeline import FeatureUnion as SKFeatureUnion
from sklearn.preprocessing import MinMaxScaler as SKMinMaxScaler
from sklearn.preprocessing import OneHotEncoder as SKOneHotEncoder

from .._checking import istype
from .._typing import PandasTypeList


# FeatureUnion doc ported with modifications from scikit-learn
# https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/pipeline.py


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


# make_union function and its doc ported with modifications from scikit-learn
# https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/pipeline.py


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


# MinMaxScaler doc ported with modifications from scikit-learn
# https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/preprocessing/_data.py


class MinMaxScaler(SKMinMaxScaler):
    """
    Transform features by scaling each feature to a given range.

    This estimator scales and translates each feature individually such
    that it is in the given range on the training set, e.g. between
    zero and one.

    The transformation is given by::

        X_std = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
        X_scaled = X_std * (max - min) + min

    where min, max = feature_range.

    This transformation is often used as an alternative to zero mean,
    unit variance scaling.

    Parameters
    ----------
    feature_range : tuple (min, max), default=(0, 1)
        Desired range of transformed data.

    copy : bool, default=True
        Set to False to perform inplace row normalization and avoid a
        copy (if the input is already a numpy array).

    clip : bool, default=False
        Set to True to clip transformed values of held-out data to
        provided `feature range`.

    Attributes
    ----------
    min_ : ndarray of shape (n_features,)
        Per feature adjustment for minimum. Equivalent to
        ``min - X.min(axis=0) * self.scale_``

    scale_ : ndarray of shape (n_features,)
        Per feature relative scaling of the data. Equivalent to
        ``(max - min) / (X.max(axis=0) - X.min(axis=0))``

    data_min_ : ndarray of shape (n_features,)
        Per feature minimum seen in the data

    data_max_ : ndarray of shape (n_features,)
        Per feature maximum seen in the data

    data_range_ : ndarray of shape (n_features,)
        Per feature range ``(data_max_ - data_min_)`` seen in the data

    n_samples_seen_ : int
        The number of samples processed by the estimator.
        It will be reset on new calls to fit, but increments across
        ``partial_fit`` calls.

    Examples
    --------
    >>> from dtoolkit.transformer import MinMaxScaler
    >>> data = [[-1, 2], [-0.5, 6], [0, 10], [1, 18]]
    >>> scaler = MinMaxScaler()
    >>> print(scaler.fit(data))
    MinMaxScaler()
    >>> print(scaler.data_max_)
    [ 1. 18.]
    >>> print(scaler.transform(data))
    [[0.   0.  ]
     [0.25 0.25]
     [0.5  0.5 ]
     [1.   1.  ]]
    >>> print(scaler.transform([[2, 2]]))
    [[1.5 0. ]]

    Notes
    -----
    Different to :obj:`sklearn.preprocessing.MinMaxScaler`.
    This would let pandas in and pandas out.
    """

    @doc(
        SKMinMaxScaler.transform,
        dedent(
            """
        Notes
        -----
        This would let pandas in and pandas out.""",
        ),
    )
    def transform(self, X, *_):
        X_new = super().transform(X, *_)

        return _change_data_to_df(X_new, X)

    @doc(
        SKMinMaxScaler.inverse_transform,
        dedent(
            """
        Notes
        -----
        This would let pandas in and pandas out.""",
        ),
    )
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
