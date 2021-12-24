from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

from dtoolkit.transformer.base import NumpyTF


if TYPE_CHECKING:
    from dtoolkit._typing import SeriesOrFrame


class RavelTF(NumpyTF):
    """
    A transformer could return a contiguous flattened array.

    This transformer is used to handle that sklearn model requires ``y``'s
    shape is ``(n, )``. But actually we always forget this. So you would get
    a ``DataConversionWarning`` ::

        DataConversionWarning: A column-vector y was passed when a 1d array
        was expected. Please change the shape of y to (n_samples, ), for
        example using ravel().

    See Also
    --------
    numpy.ravel : This transformer's prototype method.

    Examples
    --------
    >>> from dtoolkit.transformer import RavelTF
    >>> x = np.array([[1, 2, 3], [4, 5, 6]])
    >>> tf = RavelTF()

    :meth:`RavelTF.transform`, flatten data:

    >>> transformed_data = tf.transform(x)
    >>> transformed_data
    array([1, 2, 3, 4, 5, 6])

    :meth:`RavelTF.inverse_transform`, transform data to
    :class:`~pandas.Series`:

    >>> tf.inverse_transform(transformed_data).astype('int64')
    0    1
    1    2
    2    3
    3    4
    4    5
    5    6
    dtype: int64
    """

    transform_method = staticmethod(np.ravel)

    def inverse_transform(
        self,
        X: np.ndarray | SeriesOrFrame,
    ) -> pd.Series:
        """
        Transform ``X`` to a column :class:`~pandas.Series` (1D data).

        Parameters
        ----------
        X : DataFrame or array-like of shape ``(n_samples, n_features)``
            Input data that will be transformed.

        Returns
        -------
        Series
            Transformed a column data.
        """

        return pd.Series(np.ravel(X))
