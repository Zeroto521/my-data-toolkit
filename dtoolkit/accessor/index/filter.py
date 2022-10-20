from __future__ import annotations

from re import compile

import pandas as pd
from pandas.core.common import count_not_none
from pandas.core.dtypes.common import ensure_str

from dtoolkit.accessor import register_index_method


@register_index_method
def filter(
    index: pd.Index,
    /,
    items=None,
    like: str | None = None,
    regex: str | None = None,
    complement: bool = False,
) -> pd.Index:
    if count_not_none(items, like, regex) > 1:
        raise TypeError(
            "Keyword arguments `items`, `like`, or `regex` are mutually exclusive.",
        )

    if items:
        choice = lambda x: (x not in items) if complement else (x in items)
        return index.reindex((i in index for i in items if choice(i)))[0]
    elif like:
        condition = index.map(lambda x: like in ensure_str(x))
    elif regex:
        searcher = compile(regex).search
        condition = index.map(lambda x: searcher(ensure_str(x)) is not None)
    else:
        raise TypeError("Must pass either `items`, `like`, or `regex`.")

    return index[~condition] if complement else index[condition]
