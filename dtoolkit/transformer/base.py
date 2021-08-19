from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.base import TransformerMixin


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
