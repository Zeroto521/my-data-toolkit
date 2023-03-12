from typing import Literal

import pandas as pd

from dtoolkit.accessor.register import register_series_method


@register_series_method
def drop_not_duplicates(
    s: pd.Series,
    /,
    keep: Literal["first", "last", False] = "first",
) -> pd.Series:
    return s[~s.duplicated(keep=keep)]
