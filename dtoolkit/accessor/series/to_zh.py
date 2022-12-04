import pandas as pd
from typing import Literal
from pandas.api.types import is_string_dtype


from dtoolkit.accessor.register import register_series_method


@register_series_method
def to_zh(
    s: pd.Series,
    /,
    *,
    locale: Literal[
        "zh-hans",
        "zh-hant",
        "zh-cn",
        "zh-sg",
        "zh-tw",
        "zh-hk",
        "zh-my",
        "zh-mo",
    ] = "zh-cn",
    dictionary: dict = None,
) -> pd.Series:
    from zhconv import convert

    if not is_string_dtype(s):
        raise TypeError(f"Expected string dtype, but got {s.dtype!r}.")

    return s.apply(convert, locale=locale, update=dictionary)
