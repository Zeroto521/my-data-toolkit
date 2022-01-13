from __future__ import annotations

from textwrap import dedent
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
from pandas.util._decorators import doc
from sklearn.pipeline import FeatureUnion as SKFeatureUnion
from sklearn.preprocessing import MinMaxScaler as SKMinMaxScaler
from sklearn.preprocessing import OneHotEncoder as SKOneHotEncoder

from dtoolkit.accessor.dataframe import cols  # noqa
from dtoolkit.accessor.series import cols  # noqa
from dtoolkit.transformer._util import transform_array_to_frame
from dtoolkit.transformer._util import transform_series_to_frame
from dtoolkit.transformer.base import Transformer

if TYPE_CHECKING:
    from scipy.sparse import csr_matrix

    from dtoolkit._typing import SeriesOrFrame
    from dtoolkit._typing import TwoDimArray


class FeatureUnion(SKFeatureUnion, Transformer):
    """
    Concatenates results of multiple transformer objects.

    See Also
    --------
    make_union
        Convenience function for simplified feature union construction.

    Notes
    -----
    Different to :obj:`sklearn.pipeline.FeatureUnion`.
    This would let :obj:`~pandas.DataFrame` in and
    :obj:`~pandas.DataFrame` out.

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
        if all(isinstance(i, (pd.Series, pd.DataFrame)) for i in Xs):
            Xs = (i.reset_index(drop=True) for i in Xs)
            return pd.concat(Xs, axis=1)

        return super()._hstack(Xs)


def make_union(
    *transformers: list[Transformer],
    n_jobs: int | None = None,
    verbose: bool = False,
) -> FeatureUnion:
    """
    Construct a FeatureUnion from the given transformers.

    See Also
    --------
    FeatureUnion
        Class for concatenating the results of multiple transformer objects.

    Notes
    -----
    Different to :obj:`sklearn.pipeline.make_union`.
    This would let :obj:`~pandas.DataFrame` in and
    :obj:`~pandas.DataFrame` out.

    Examples
    --------
    >>> from sklearn.decomposition import PCA, TruncatedSVD
    >>> from dtoolkit.transformer import make_union
    >>> make_union(PCA(), TruncatedSVD())
     FeatureUnion(transformer_list=[('pca', PCA()),
                                   ('truncatedsvd', TruncatedSVD())])
    """
    from sklearn.pipeline import _name_estimators

    return FeatureUnion(
        _name_estimators(transformers),
        n_jobs=n_jobs,
        verbose=verbose,
    )


class MinMaxScaler(SKMinMaxScaler):
    """
    Transform features by scaling each feature to a given range.

    The transformation is given by::

        X_std = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
        X_scaled = X_std * (max - min) + min

    where :exc:`min, max = feature_range`.

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
    This would let :obj:`~pandas.DataFrame` in and
    :obj:`~pandas.DataFrame` out.
    """

    def transform(self, X: TwoDimArray) -> TwoDimArray:
        """
        Scale features of X according to feature_range.

        Parameters
        ----------
        X : DataFrame or array-like of shape `(n_samples, n_features)`
            Input data that will be transformed.

        Returns
        -------
        DataFrame or ndarray of shape `(n_samples, n_features)`
            Transformed data.

        Notes
        -----
        This would let :obj:`~pandas.DataFrame` in and
        :obj:`~pandas.DataFrame` out.
        """

        X_new = super().transform(X)

        return transform_array_to_frame(X_new, X)

    def inverse_transform(self, X: SeriesOrFrame | np.ndarray) -> TwoDimArray:
        """
        Undo the scaling of X according to feature_range.

        Parameters
        ----------
        X : Series, DataFrame or array-like of shape `(n_samples, n_features)`
            Input data that will be transformed. It cannot be sparse.

        Returns
        -------
        DataFrame or ndarray of shape (n_samples, n_features)
            Transformed data.

        Notes
        -----
        This would let :obj:`~pandas.DataFrame` in and
        :obj:`~pandas.DataFrame` out.
        """

        X = transform_series_to_frame(X)
        X_new = super().inverse_transform(X)

        return transform_array_to_frame(X_new, X)


class OneHotEncoder(SKOneHotEncoder):
    """
    Encode categorical features as a one-hot numeric array.

    Notes
    -----
    Different to :obj:`sklearn.preprocessing.OneHotEncoder`.
    The result would return a :obj:`~pandas.DataFrame` which uses categories
    as columns.

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

    :obj:`~pandas.DataFrame` in, :obj:`~pandas.DataFrame` out with categories
    as columns.

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

    @doc(SKOneHotEncoder.__init__)
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
        This would let :obj:`~pandas.DataFrame` out.
        """,
        ),
    )
    def transform(self, X: TwoDimArray) -> TwoDimArray | csr_matrix:
        from itertools import chain

        X_new = super().transform(X)

        if self.sparse is False:
            categories = (
                self.get_feature_names(X.cols())
                if self.categories_with_parent
                else chain.from_iterable(self.categories_)
            )

            return pd.DataFrame(X_new, columns=categories)

        return X_new
