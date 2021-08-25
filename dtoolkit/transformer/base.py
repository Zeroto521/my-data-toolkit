from __future__ import annotations

from textwrap import dedent

import numpy as np
import pandas as pd
from pandas.util._decorators import doc
from sklearn.base import TransformerMixin

from .._checking import check_dataframe_type
from .._typing import Pd


class Transformer(TransformerMixin):
    """Base class for all transformers in :class:`dtoolkit.transformer`."""

    def __init__(self, *args, **kwargs):
        """
        Transformer arguement entry.
        """

        self.args = args
        self.kwargs = kwargs

    def fit(self, *_):
        """
        Fit transformer.

        Returns
        -------
        self
            This estimator
        """

        return self

    def inverse_transform(
        self,
        X: pd.DataFrame | np.ndarray,
    ) -> pd.DataFrame | np.ndarray:
        """
        Undo transform to ``X``.

        Parameters
        ----------
        X : DataFrame or array-like of shape ``(n_samples, n_features)``
            Input data that will be transformed.

        Returns
        -------
        DataFrame or ndarray of shape ``(n_samples, n_features)``
            Transformed data.

        Notes
        -----
        This function default do **nothing** to ``X``. So it will return
        itself. The function aim is to keep the pipeline don't break without
        :func:`inverse_transform`.
        """

        return X


class MethodTF(Transformer):
    transform_method: callable
    inverse_transform_method: callable | None = None

    def transform(self, X: Pd | np.ndarray) -> pd.DataFrame | np.ndarray:
        """
        Transform ``X``.

        Parameters
        ----------
        X : Series, DataFrame or array-like
            Input data to be transformed.

        Returns
        -------
        DataFrame or ndarray
            A new X was transformed.
        """

        return self.transform_method(X, *self.args, **self.kwargs)

    @doc(Transformer.inverse_transform)
    def inverse_transform(
        self,
        X: pd.DataFrame | np.ndarray,
    ) -> pd.DataFrame | np.ndarray:
        if self.inverse_transform_method:
            return self.inverse_transform_method(X)

        return super().inverse_transform(X)


class NumpyTF(MethodTF):
    """
    Base class for all :mod:`numpy` transformers in
    :class:`dtoolkit.transformer`.
    """


class DataFrameTF(MethodTF):
    """
    Base class for all :class:`~pandas.DataFrame` transformers in
    :class:`dtoolkit.transformer`.
    """

    @doc(
        MethodTF.__init__,
        dedent(
            """
        Notes
        -----
        If ``kwargs`` have ``inplace`` parameter, it would be remove autoly.
        The inplace parameter is not work for DataFrame transformer. Actually
        this would break pipeline stream. If a transformer's inplace is True,
        the next tf input would get None.""",
        ),
    )
    def __init__(self, *args, **kwargs):
        kwargs.pop("inplace", None)
        super().__init__(*args, **kwargs)
