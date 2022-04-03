from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

from dtoolkit.accessor._util import collapse
from dtoolkit.accessor.drop_or_not import drop_or_not  # noqa
from dtoolkit.accessor.register import register_dataframe_method
from dtoolkit.accessor.series import values_to_dict as s_values_to_dict  # noqa

if TYPE_CHECKING:
    from dtoolkit._typing import IntOrStr
    from sklearn.base import TransformerMixin


@register_dataframe_method
def decompose(
    df: pd.DataFrmae,
    method: TransformerMixin,
    columns: pd.Series
    | dict[IntOrStr | tuple[IntOrStr], list[IntOrStr] | tuple[IntOrStr]]
    | list[IntOrStr]
    | tuple[IntOrStr]
    | None = None,
    drop: bool = False,
    inplace: bool = False,
    **kwargs,
) -> pd.DataFrame | None:
    """
    Decompose DataFrame's columns.

    Parameters
    ----------
    method : TransformerMixin
        :class:`sklearn.decomposition`

    columns : dict, Series, list, tuple or None, default None
        Choose columns to decompose.

        - None: Decompose all columns.
        - list or tuple: Decompose the selected columns.
        - dict or Series: Decompose and remap columns to a few.

    drop : bool, default False
        If True, drop the used columns.

    inplace : bool, default False
        If True, do operation inplace and return None.

    **kwargs
        See the documentation for ``method`` for complete details on
        the keyword arguments.

    Returns
    -------
    DataFrame or None
        If inplace is False will return the decomposed data.

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
    ...         [3, 2, -3, -2]
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

    >>> df.decompose(decomposition.PCA)
              a         b             c             d
    0  1.956431  0.415183  9.009015e-17  8.100537e-18
    1  3.142238 -0.355441  8.394617e-17  9.817066e-18
    2  5.098670  0.059742 -8.445140e-17  1.640353e-19
    3 -1.956431 -0.415183 -7.881266e-17  8.428608e-18
    4 -3.142238  0.355441 -8.495664e-17  1.014514e-17
    5 -5.098670 -0.059742  8.445140e-17 -1.640353e-19

    Decompose the selected columns.

    >>> df.decompose(decomposition.PCA, ["a", "b"])
              a         b  c  d
    0  1.383406  0.293579  1  1
    1  2.221898 -0.251335  2  1
    2  3.605304  0.042244  3  2
    3 -1.383406 -0.293579 -1 -1
    4 -2.221898  0.251335 -2 -1
    5 -3.605304 -0.042244 -3 -2

    Decompose and remap columns to a few.

    >>> df.decompose(decomposition.PCA, {"A": ["a", "b"], "B": ["b", "c", "d"]})
              A         B  a  b  c  d
    0  1.383406  1.694316 -1 -1  1  1
    1  2.221898  2.428593 -2 -1  2  1
    2  3.605304  4.122909 -3 -2  3  2
    3 -1.383406 -1.694316  1  1 -1 -1
    4 -2.221898 -2.428593  2  1 -2 -1
    5 -3.605304 -4.122909  3  2 -3 -2
    >>> df.decompose(decomposition.PCA, {("A", "B"): ["a", "b", "c"]})
              A         B  a  b  c  d
    0  1.702037  0.321045 -1 -1  1  1
    1  2.988071 -0.267273 -2 -1  2  1
    2  4.690108  0.053773 -3 -2  3  2
    3 -1.702037 -0.321045  1  1 -1 -1
    4 -2.988071  0.267273  2  1 -2 -1
    5 -4.690108 -0.053773  3  2 -3 -2

    The ``columns`` also accecpt Series.

    >>> s = pd.Series(["a", "b"], index=["A", "A"])
    >>> s
    A    a
    A    b
    dtype: object
    >>> df.decompose(decomposition.PCA, s, drop=True)
              A  c  d
    0  1.383406  1  1
    1  2.221898  2  1
    2  3.605304  3  2
    3 -1.383406 -1 -1
    4 -2.221898 -2 -1
    5 -3.605304 -3 -2
    """

    if columns is None:
        result = pd.DataFrame(
            method(*kwargs).fit_transform(df),
            index=df.index,
            columns=df.columns,
        )

    if isinstance(columns, (list, tuple)):
        result = pd.DataFrame(
            method(*kwargs).fit_transform(df[columns]),
            index=df.index,
            columns=columns,
        ).combine_first(
            df.drop_or_not(
                drop=drop,
                columns=columns,
            ),
        )

    elif isinstance(columns, (dict, pd.Series)):
        if isinstance(columns, pd.Series):
            columns = columns.values_to_dict()

        result = pd.DataFrame(
            np.hstack(
                [
                    method(
                        len(key) if isinstance(key, tuple) else 1,
                        **kwargs,
                    ).fit_transform(df[value])
                    for key, value in columns.items()
                ],
            ),
            index=df.index,
            columns=list(collapse(columns.keys())),
        ).combine_first(
            df.drop_or_not(
                drop=drop,
                columns=list(collapse(columns.values())),
            ),
        )

    if not inplace:
        return result

    df._update_inplace(result)
