from __future__ import annotations

from textwrap import dedent
from typing import Any
from typing import Callable

import numpy as np
import pandas as pd
from pandas.util._decorators import doc
from sklearn.base import TransformerMixin

from dtoolkit._typing import SeriesOrFrame
from dtoolkit.transformer._util import transform_frame_to_series
from dtoolkit.transformer._util import transform_series_to_frame
from dtoolkit.transformer._validation import require_series_or_frame


class Transformer(TransformerMixin):
    """Base class for all transformers in :class:`dtoolkit.transformer`."""

    def inverse_transform(self, X: Any) -> Any:
        """
        Undo transform to ``X``.

        Notes
        -----
        This function default do **nothing** to ``X``. So it will return
        itself. The function aim is to keep the pipeline don't break without
        :func:`inverse_transform`.
        """

        return X


class MethodTF(Transformer):
    """
    Base class for all method transformers in :class:`dtoolkit.transformer`.
    """

    transform_method: Callable
    inverse_transform_method: Callable = None

    def __init__(self, *args, **kwargs):
        """Transform method argument entry."""

        # transform method parameters
        self.args = args
        self.kwargs = kwargs

        # inverse transform parameters
        self.inverse_args = ()
        self.inverse_kwargs = {}

    def fit(self, *_):
        """
        Fit transformer.

        Returns
        -------
        self
            This estimator
        """

        return self

    def update_invargs(self, *args, **kwargs):
        """Inverse transform method argument entry."""

        self.inverse_args = args or self.inverse_args
        self.inverse_kwargs.update(kwargs)

        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        """
        Transform ``X``.

        Parameters
        ----------
        X : array-like
            Input data to be transformed.

        Returns
        -------
        ndarray
            A new X was transformed.
        """

        X = transform_series_to_frame(X)

        Xt = self.transform_method(X, *self.args, **self.kwargs)
        return transform_frame_to_series(Xt)

    def inverse_transform(self, X: np.ndarray) -> np.ndarray:
        """
        Undo transform to ``X``.

        Parameters
        ----------
        X : array-like of shape ``(n_samples, n_features)``
            Input data that will be transformed.

        Returns
        -------
        ndarray
            Transformed data.

        Notes
        -----
        If ``inverse_transform_method`` is None, there would do nothing for
        ``X``.
        """

        if self.inverse_transform_method:
            Xt = self.inverse_transform_method(
                transform_series_to_frame(X),
                *self.inverse_args,
                **self.inverse_kwargs,
            )
            return transform_frame_to_series(Xt)

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
        the next tf input would get None.
        """,
        ),
    )
    def __init__(self, *args, **kwargs):
        kwargs.pop("inplace", None)
        super().__init__(*args, **kwargs)

    def transform(self, X: SeriesOrFrame) -> pd.DataFrame:
        """
        Transform ``X``.

        Parameters
        ----------
        X : Series or DataFrame
            Input data to be transformed.

        Returns
        -------
        DataFrame
            A new X was transformed.
        """

        require_series_or_frame(X)

        return super().transform(X)

    def inverse_transform(self, X: SeriesOrFrame) -> SeriesOrFrame:
        """
        Undo transform to ``X``.

        Parameters
        ----------
        X : Series or DataFrame
            Input data that will be transformed.

        Returns
        -------
        DataFrame
            Transformed data.

        Notes
        -----
        If ``inverse_transform_method`` is None, there would do nothing for
        ``X``.
        """

        require_series_or_frame(X)

        return super().inverse_transform(X)
