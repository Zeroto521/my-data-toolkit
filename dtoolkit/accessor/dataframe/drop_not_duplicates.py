from typing import Literal
from typing import Hashable
from typing import Sequence

import pandas as pd

from dtoolkit.accessor.register import register_dataframe_method


@register_dataframe_method
def drop_not_duplicates(
    df: pd.DataFrame,
    /,
    subset: Hashable | Sequence[Hashable] | None = None,
    keep: Literal["first", "last", False] = "first",
) -> pd.DataFrame:
    return df[~df.duplicated(subset=subset, keep=keep)]
