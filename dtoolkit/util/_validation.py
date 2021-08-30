from __future__ import annotations

from typing import Any

import pandas as pd


def istype(var: Any, types: type | list[type] | tuple[type]) -> bool:
    types: tuple[type] = containerize(types, tuple)

    return isinstance(var, types)


def containerize(var: Any, finaltype=list) -> list[Any] | tuple[Any]:
    if not isinstance(var, (list, tuple)):
        var = [var]

    return finaltype(var)


def check_dataframe_type(df: pd.DataFrame):
    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            "The input is not a 'DataFrame' type.",
        )
