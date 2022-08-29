from __future__ import annotations

from textwrap import dedent
from typing import Hashable

import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.accessor.register import register_dataframe_method
from dtoolkit.accessor.series import expand as s_expand


@register_dataframe_method
@doc(
    s_expand,
    examples=dedent(
        """
    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> import numpy as np

    Expand the *list-like* element.

    >>> df = pd.DataFrame(
    ...     {
    ...         'A': [[0, 1, 2], 'foo', [], [3, 4]],
    ...         'B': 1,
    ...         'C': [['a', 'b', 'c'], np.nan, [], ['d', 'e']],
    ...     },
    ... )
    >>> df.expand()
        A_0  A_1  A_2  B   C_0   C_1   C_2
    0     0  1.0  2.0  1     a     b     c
    1   foo  NaN  NaN  1   NaN  None  None
    2  None  NaN  NaN  1  None  None  None
    3     3  4.0  NaN  1     d     e  None

    Expand *sub-element* type is list-like.

    >>> df = pd.DataFrame({"col1": [1, 2], "col2": [("a", "b"), (3, (5, 6))]})
    >>> df.expand(flatten=True)
       col1 col2_0 col2_1  col2_2
    0     1      a      b     NaN
    1     2      3      5     6.0

    Set the columns of name.

    >>> df = pd.DataFrame({"col1": [1, 2], "col2": [("a", 3), ("b", 4)]})
    >>> df.expand(suffix=["index", "value"], delimiter="-")
       col1  col2-index  col2-value
    0     1           a           3
    1     2           b           4

    Also could handle **different lengths** of element and suffix list.

    >>> df = pd.DataFrame({"col1": [1, 2], "col2": [(3, 4), (5, 6, 7)]})
    >>> df.expand()
       col1  col2_0  col2_1  col2_2
    0     1       3       4     NaN
    1     2       5       6     7.0
    >>> df.expand(suffix=["a", "b", "c", "d"])
       col1  col2_a  col2_b  col2_c
    0     1       3       4     NaN
    1     2       5       6     7.0
    """,
    ),
)
def expand(
    df: pd.DataFrame,
    /,
    suffix: list[Hashable] = None,
    delimiter: str = "_",
    flatten: bool = False,
) -> pd.DataFrame:

    return pd.concat(
        (
            s_expand(
                s,
                suffix=suffix,
                delimiter=delimiter,
                flatten=flatten,
            )
            for _, s in df.items()
        ),
        axis=1,
    )
