from __future__ import annotations

import pandas as pd


def validate_axis(df: pd.DataFrame, axis: int | str) -> int:
    if isinstance(axis, (tuple, list)):
        msg = "supplying multiple axes to axis is no longer supported."
        raise TypeError(msg)

    return df._get_axis_number(axis)
