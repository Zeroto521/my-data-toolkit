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
from ..accessor import ColumnAccessor  # noqa

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
    >>> scaler.fit(data)
    MinMaxScaler()
    >>> scaler.data_max_
    array([ 1., 18.])
    >>> scaler.transform(data)
    array([[0.  , 0.  ],
           [0.25, 0.25],
           [0.5 , 0.5 ],
           [1.  , 1.  ]])
    >>> scaler.transform([[2, 2]])
    array([[1.5, 0. ]])

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


# OneHotEncoder doc ported with modifications from scikit-learn
# https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/preprocessing/_encoders.py


class OneHotEncoder(SKOneHotEncoder):
    """
    Encode categorical features as a one-hot numeric array.

    The input to this transformer should be an array-like of integers or
    strings, denoting the values taken on by categorical (discrete) features.
    The features are encoded using a one-hot (aka 'one-of-K' or 'dummy')
    encoding scheme. This creates a binary column for each category and
    returns a sparse matrix or dense array (depending on the ``sparse``
    parameter)

    By default, the encoder derives the categories based on the unique values
    in each feature. Alternatively, you can also specify the `categories`
    manually.

    This encoding is needed for feeding categorical data to many scikit-learn
    estimators, notably linear models and SVMs with the standard kernels.

    Note: a one-hot encoding of y labels should use a `LabelBinarizer`
    instead.

    Parameters
    ----------
    categories : 'auto' or a list of array-like, default='auto'
        Categories (unique values) per feature:

        - 'auto' : Determine categories automatically from the training data.
        - list : ``categories[i]`` holds the categories expected in the ith
          column. The passed categories should not mix strings and numeric
          values within a single feature, and should be sorted in case of
          numeric values.

        The used categories can be found in the ``categories_`` attribute.

    categories_with_parent: bool, default=False
        The return DataFrame columns will hook DataFrame.columns if set True
        else will the return DataFrame columns only with categories.

    drop : {'first', 'if_binary'} or a array-like of shape (n_features,), \
            default=None
        Specifies a methodology to use to drop one of the categories per
        feature. This is useful in situations where perfectly collinear
        features cause problems, such as when feeding the resulting data
        into a neural network or an unregularized regression.

        However, dropping one category breaks the symmetry of the original
        representation and can therefore induce a bias in downstream models,
        for instance for penalized linear classification or regression models.

        - None : retain all features (the default).
        - 'first' : drop the first category in each feature. If only one
          category is present, the feature will be dropped entirely.
        - 'if_binary' : drop the first category in each feature with two
          categories. Features with 1 or more than 2 categories are
          left intact.
        - array : ``drop[i]`` is the category in feature ``X[:, i]`` that
          should be dropped.

    sparse : bool, default=False
        Will return sparse matrix if set True else will return an array.

    dtype : number type, default=float
        Desired dtype of output.

    handle_unknown : {'error', 'ignore'}, default='error'
        Whether to raise an error or ignore if an unknown categorical feature
        is present during transform (default is to raise). When this parameter
        is set to 'ignore' and an unknown category is encountered during
        transform, the resulting one-hot encoded columns for this feature
        will be all zeros. In the inverse transform, an unknown category
        will be denoted as None.

    Attributes
    ----------
    categories_ : list of arrays
        The categories of each feature determined during fitting
        (in order of the features in X and corresponding with the output
        of ``transform``). This includes the category specified in ``drop``
        (if any).

    drop_idx_ : array of shape (n_features,)
        - ``drop_idx_[i]`` is the index in ``categories_[i]`` of the category
          to be dropped for each feature.
        - ``drop_idx_[i] = None`` if no category is to be dropped from the
          feature with index ``i``, e.g. when `drop='if_binary'` and the
          feature isn't binary.
        - ``drop_idx_ = None`` if all the transformed features will be
          retained.

    Notes
    -----
    Different to :obj:`sklearn.preprocessing.MinMaxScaler`.
    The result would return a DataFrame which uses categories as columns.

    Examples
    --------
    Given a dataset with two features, we let the encoder find the unique
    values per feature and transform the data to a binary one-hot encoding.

    >>> from dtoolkit.transformer import OneHotEncoder

    One can discard categories not seen during `fit`:

    >>> enc = OneHotEncoder(sparse=True, handle_unknown='ignore')
    >>> X = [['Male', 1], ['Female', 3], ['Female', 2]]
    >>> enc.fit(X)
    OneHotEncoder(handle_unknown='ignore', sparse=True)
    >>> enc.categories_
    [array(['Female', 'Male'], dtype=object), array([1, 2, 3], dtype=object)]
    >>> enc.transform([['Female', 1], ['Male', 4]]).toarray()
    array([[1., 0., 1., 0., 0.],
           [0., 1., 0., 0., 0.]])
    >>> enc.inverse_transform([[0, 1, 1, 0, 0], [0, 0, 0, 1, 0]])
    array([['Male', 1],
           [None, 2]], dtype=object)
    >>> enc.get_feature_names(['gender', 'group'])
    array(['gender_Female', 'gender_Male', 'group_1', 'group_2', 'group_3'],
      dtype=object)

    One can always drop the first column for each feature:

    >>> drop_enc = OneHotEncoder(sparse=True, drop='first').fit(X)
    >>> drop_enc.categories_
    [array(['Female', 'Male'], dtype=object), array([1, 2, 3], dtype=object)]
    >>> drop_enc.transform([['Female', 1], ['Male', 2]]).toarray()
    array([[0., 0., 0.],
           [1., 1., 0.]])

    Or drop a column for feature only having 2 categories:

    >>> drop_binary_enc = OneHotEncoder(sparse=True, drop='if_binary').fit(X)
    >>> drop_binary_enc.transform([['Female', 1], ['Male', 2]]).toarray()
    array([[0., 1., 0., 0.],
           [1., 0., 1., 0.]])

    Pandas DataFrame in, Pandas DataFrame out with categories as columns.

    >>> import pandas as pd
    >>> df = pd.DataFrame(X, columns=['gender', 'number'])
    >>> df
        gender  number
    0    Male       1
    1  Female       3
    2  Female       2
    >>> enc = OneHotEncoder(categories_with_parent=True)
    >>> enc.fit_transform(df)
    gender_Female  gender_Male  number_1  number_2  number_3
    0            0.0          1.0       1.0       0.0       0.0
    1            1.0          0.0       0.0       0.0       1.0
    2            1.0          0.0       0.0       1.0       0.0
    """

    def __init__(
        self,
        categories="auto",
        categories_with_parent=False,
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
        self.categories_with_parent = categories_with_parent

    @doc(
        SKOneHotEncoder.transform,
        dedent(
            """
        Notes
        -----
        This would let pandas in and pandas out.""",
        ),
    )
    def transform(self, X, *_):
        X_new = super().transform(X, *_)

        if self.sparse is False:
            categories = (
                self.get_feature_names(X.cols())
                if self.categories_with_parent
                else flatten(self.categories_)
            )

            return pd.DataFrame(X_new, columns=categories)

        return X_new
