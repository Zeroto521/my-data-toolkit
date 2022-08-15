from typing import Literal

import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.accessor.register import register_dataframe_method
from dtoolkit.accessor.series import dropna_index as s_dropna_index


@register_dataframe_method
@doc(s_dropna_index, klass="DataFrame")
def dropna_index(
    df: pd.DataFrame,
    /,
    how: Literal["any", "all"] = "any",
) -> pd.DataFrame:
    return s_dropna_index(df, how=how)
