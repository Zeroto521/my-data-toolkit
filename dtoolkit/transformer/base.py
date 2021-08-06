from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from sklearn.base import TransformerMixin

from .._typing import Pd


class Transformer(TransformerMixin):
    """Base class for all transformers in dtoolkit."""

    def __init__(self, *args, **kwargs):
        """
        Transformer arguement entry.

        Parameters
        ----------
        args
            The positional arguements of :func:`~Transformer.operate`.
        kwargs
            The keyword arguements of :func:`~Transformer.operate`.
        """

        self.args = args
        self.kwargs = kwargs

    def operate(self, X: Pd | np.ndarray, *_, **__) -> Pd | np.ndarray:
        """
        The backend algorithm of :func:`Transformer.transform`.

        Parameters
        ----------
        X : Series, DataFrame or array-like
            Input data to be transformed. The same one to
            :func:`~Transformer.transform`.
        _
            The positional arguements of its.
        __
            The keyword arguements of its.

        Returns
        -------
        DataFrame or ndarray
            A new X was transformed.

        Notes
        -----
        The subclass should implement its own method.
        """

        return X

    def validate(self, X: Any):
        """
        It should validate the type of ``X``before ``X`` transformed.

        Parameters
        ----------
        X
            Input data to be transformed. The same one to
            :func:`~Transformer.transform`.

        Notes
        -----
        The subclass should implement its own method.
        """
        ...

    def fit(self, *_):
        """
        Fit transformer.

        Returns
        -------
        self
            This estimator
        """

        return self

    def transform(self, X: Pd | np.ndarray, *_) -> Pd | np.ndarray:
        """Transform X separately by each transformer, concatenate results.

        Parameters
        ----------
        X : Series, DataFrame or array-like
            Input data to be transformed.

        Returns
        -------
        DataFrame or ndarray
            A new X was transformed via :func:`~Transformer.operate`.
        """

        self.validate(X)

        return self.operate(X, *self.args, **self.kwargs)

    def inverse_transform(
        self, X: pd.DataFrame | np.ndarray
    ) -> pd.DataFrame | np.ndarray:
        """
        Undo transform to X.

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
