from __future__ import annotations

from itertools import chain
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

from dtoolkit._typing import IntOrStr
from dtoolkit.accessor.dataframe import drop_or_not  # noqa
from dtoolkit.accessor.register import register_dataframe_method

if TYPE_CHECKING:
    from sklearn.base import TransformerMixin


@register_dataframe_method
def decompose(
    df: pd.DataFrmae,
    method: TransformerMixin,
    columns: None
    | dict[IntOrStr | tuple[IntOrStr], IntOrStr | list[IntOrStr] | tuple[IntOrStr]]
    | list[IntOrStr]
    | pd.Index = None,
    drop: bool = False,
    **kwargs,
) -> pd.DataFrame:
    """
    Decompose DataFrame's columns.

    Parameters
    ----------
    method : TransformerMixin
        Decomposition transformer.

    columns : dict, Series, list, tuple or None, default None
        Choose columns to decompose.

        - None : Decompose all columns.
        - list or Index : Decompose the selected columns.
        - dict : Decompose and remap columns to a few, ``{new columns: old columns}``.

    drop : bool, default False
        If True, drop the used columns when ``columns`` is :keyword:`dict`.

    **kwargs
        See the documentation for ``method`` for complete details on
        the keyword arguments.

    Returns
    -------
    DataFrame

    See Also
    --------
    sklearn.decomposition
        Scikit-learn's matrix decomposition transformer.

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> from sklearn import decomposition
    >>> df = pd.DataFrame(
    ...     [
    ...         [-1, -1, 1, 1],
    ...         [-2, -1, 2, 1],
    ...         [-3, -2, 3, 2],
    ...         [1, 1, -1, -1],
    ...         [2, 1, -2, -1],
    ...         [3, 2, -3, -2],
    ...     ],
    ...     columns=["a", "b", "c", "d"],
    ... )
    >>> df
       a  b  c  d
    0 -1 -1  1  1
    1 -2 -1  2  1
    2 -3 -2  3  2
    3  1  1 -1 -1
    4  2  1 -2 -1
    5  3  2 -3 -2

    Decompose all columns.

    >>> df.decompose(decomposition.PCA)  # doctest: +SKIP
              a         b             c             d
    0  1.956431  0.415183  9.009015e-17  8.100537e-18
    1  3.142238 -0.355441  8.394617e-17  9.817066e-18
    2  5.098670  0.059742 -8.445140e-17  1.640353e-19
    3 -1.956431 -0.415183 -7.881266e-17  8.428608e-18
    4 -3.142238  0.355441 -8.495664e-17  1.014514e-17
    5 -5.098670 -0.059742  8.445140e-17 -1.640353e-19

    Decompose the selected columns.

    >>> df.decompose(decomposition.PCA, ["a", "b"])  # doctest: +SKIP
              a         b  c  d
    0  1.383406  0.293579  1  1
    1  2.221898 -0.251335  2  1
    2  3.605304  0.042244  3  2
    3 -1.383406 -0.293579 -1 -1
    4 -2.221898  0.251335 -2 -1
    5 -3.605304 -0.042244 -3 -2

    Decompose and remap columns to a few.

    >>> df.decompose(
    ...     decomposition.PCA,
    ...     {"A": ["a", "b"], "B": ["b", "c", "d"]},
    ... )  # doctest: +SKIP
              A         B  a  b  c  d
    0  1.383406  1.694316 -1 -1  1  1
    1  2.221898  2.428593 -2 -1  2  1
    2  3.605304  4.122909 -3 -2  3  2
    3 -1.383406 -1.694316  1  1 -1 -1
    4 -2.221898 -2.428593  2  1 -2 -1
    5 -3.605304 -4.122909  3  2 -3 -2
    >>> df.decompose(
    ...     decomposition.PCA,
    ...     {("A", "B"): ["a", "b", "c"]}
    ... )  # doctest: +SKIP
              A         B  a  b  c  d
    0  1.702037  0.321045 -1 -1  1  1
    1  2.988071 -0.267273 -2 -1  2  1
    2  4.690108  0.053773 -3 -2  3  2
    3 -1.702037 -0.321045  1  1 -1 -1
    4 -2.988071  0.267273  2  1 -2 -1
    5 -4.690108 -0.053773  3  2 -3 -2
    """

    if columns is None:
        return pd.DataFrame(
            _decompose(method, df, **kwargs),
            index=df.index,
            columns=df.columns,
        )

    elif isinstance(columns, (list, pd.Index)):
        return pd.DataFrame(
            _decompose(method, df[columns], **kwargs),
            index=df.index,
            columns=columns,
        ).combine_first(df)

    elif isinstance(columns, dict):
        return pd.DataFrame(
            np.hstack(
                [
                    _decompose(
                        method,
                        df[value],
                        n_components=len(key) if isinstance(key, tuple) else 1,
                        **kwargs,
                    )
                    for key, value in columns.items()
                ],
            ),
            index=df.index,
            columns=chain.from_iterable(columns.keys()),
        ).combine_first(
            df.drop_or_not(
                drop=drop,
                columns=chain.from_iterable(columns.values()),
            ),
        )

    raise ValueError("The type of inputting 'columns' isn't right")


def _decompose(
    method: TransformerMixin,
    df: pd.DataFrame,
    n_components=None,
    **kwargs,
) -> np.ndarray:
    if n_components is None and len(df) < len(df.columns):
        raise ValueError(
            "Don't support decomposing DataFrame in which "
            "the number of rows is less than the number of columns",
        )

    return method(n_components, **kwargs).fit_transform(
        df.to_frame() if isinstance(df, pd.Series) else df,
    )
