from __future__ import annotations

from textwrap import dedent
from typing import TYPE_CHECKING

import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.accessor.register import register_dataframe_method
from dtoolkit.accessor.series import cols as s_cols


if TYPE_CHECKING:
    from dtoolkit._typing import IntOrStr


@register_dataframe_method
@doc(
    s_cols,
    returns=dedent(
        """
    Returns
    -------
    list of str or int
        The column names.
    """,
    ),
)
def cols(df: pd.DataFrame) -> list[IntOrStr]:
    return df.columns.tolist()
