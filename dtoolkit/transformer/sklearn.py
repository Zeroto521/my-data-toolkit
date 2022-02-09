from __future__ import annotations

from textwrap import dedent
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
from pandas.util._decorators import doc
from sklearn.preprocessing import MinMaxScaler as SKMinMaxScaler
from sklearn.preprocessing import OneHotEncoder as SKOneHotEncoder

from dtoolkit.accessor.dataframe import cols  # noqa
from dtoolkit.accessor.series import cols  # noqa
from dtoolkit.transformer._util import transform_array_to_frame
from dtoolkit.transformer._util import transform_frame_to_series
from dtoolkit.transformer._util import transform_series_to_frame

if TYPE_CHECKING:
    from scipy.sparse import csr_matrix

    from dtoolkit._typing import SeriesOrFrame
    from dtoolkit._typing import TwoDimArray


class MinMaxScaler(SKMinMaxScaler):
    """
    Transform features by scaling each feature to a given range.

    .. warning::
        Transformer :class:`dtoolkit.transformer.MinMaxScaler` is deprecated and
        will be removed in 0.0.13.
        Please use :class:`sklearn.preprocessing.MinMaxScaler` instead.
        (Warning added DToolKit 0.0.12)

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

    @doc(SKMinMaxScaler.__init__)
    def __init__(self, feature_range=(0, 1), *, copy=True, clip=False):
        from warnings import warn

        warn(
            "Transformer 'dtoolkit.transformer.MinMaxScaler' is deprecated and "
            "will be removed in 0.0.13. "
            "Please use 'sklearn.preprocessing.MinMaxScaler' instead. "
            "(Warning added DToolKit 0.0.12)",
            DeprecationWarning,
        )

        super().__init__(
            feature_range=feature_range,
            copy=copy,
            clip=clip,
        )

    @doc(SKMinMaxScaler.fit)
    def fit(self, X, y=None):
        X = transform_series_to_frame(X)

        return super().fit(X, y)

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

        X = transform_series_to_frame(X)
        Xt = super().transform(X)
        Xt = transform_array_to_frame(Xt, X)

        return transform_frame_to_series(Xt)

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
        Xt = super().inverse_transform(X)
        Xt = transform_array_to_frame(Xt, X)

        return transform_frame_to_series(Xt)


class OneHotEncoder(SKOneHotEncoder):
    """
    Encode categorical features as a one-hot numeric array.

    Parameters
    ----------
    categories_with_parent : bool, default False
        Returned column would hook parent labels if ``True`` else
        would be ``categories``.

    sparse : bool, default False
        Will return sparse matrix if ``True`` else will return an array.

    kwargs
        See :obj:`sklearn.preprocessing.OneHotEncoder`.

    Notes
    -----
    Different to :obj:`sklearn.preprocessing.OneHotEncoder`.
    The result would return a :obj:`~pandas.DataFrame` which uses categories
    as columns.

    Examples
    --------
    Given a dataset with two features, we let the encoder find the unique
    values per feature and transform the data to a binary one-hot encoding.

    :obj:`~pandas.DataFrame` in, :obj:`~pandas.DataFrame` out with categories
    as columns.

    >>> from dtoolkit.transformer import OneHotEncoder
    >>> import pandas as pd
    >>> X = [['Male', 1], ['Female', 3], ['Female', 2]]
    >>> df = pd.DataFrame(X, columns=['gender', 'number'])
    >>> df
        gender  number
    0    Male       1
    1  Female       3
    2  Female       2
    >>> enc = OneHotEncoder()
    >>> enc.fit_transform(df)
       Female  Male    1    2    3
    0     0.0   1.0  1.0  0.0  0.0
    1     1.0   0.0  0.0  0.0  1.0
    2     1.0   0.0  0.0  1.0  0.0

    The encoded data also could hook parent labels.

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
        categories_with_parent: bool = False,
        sparse: bool = False,
        **kwargs,
    ):
        super().__init__(sparse=sparse, **kwargs)
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

        Xt = super().transform(X)

        if self.sparse is False:
            categories = (
                self.get_feature_names_out(X.cols())
                if self.categories_with_parent
                else chain.from_iterable(self.categories_)
            )

            return pd.DataFrame(Xt, columns=categories)

        return Xt
