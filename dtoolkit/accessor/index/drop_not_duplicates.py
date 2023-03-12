from typing import Literal

import pandas as pd

from dtoolkit.accessor.register import register_index_method


@register_index_method
def drop_not_duplicates(
    index: pd.Index,
    /,
    keep: Literal["first", "last", False] = "first",
) -> pd.Index:
    return index[~index.duplicated(keep=keep)]
