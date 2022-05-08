from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

if TYPE_CHECKING:
    from typing import Iterable

    from dtoolkit._typing import IntOrStr
    from dtoolkit._typing import OneDimArray
    from dtoolkit._typing import SeriesOrFrame
    from dtoolkit._typing import TwoDimArray


def get_inf_range(inf: str = "all") -> list[float]:
    if inf == "all":
        return [np.inf, -np.inf]
    elif inf == "pos":
        return [np.inf]
    elif inf == "neg":
        return [-np.inf]
    elif inf is not None:
        raise ValueError(f"invalid inf option: {inf!r}")

    raise TypeError("must specify inf")


def get_mask(how: str, mask: TwoDimArray, axis: int) -> OneDimArray:
    if how == "any":
        return mask.any(axis=axis)
    elif how == "all":
        return mask.all(axis=axis)
    elif how is not None:
        raise ValueError(f"invalid inf option: {how!r}")

    raise TypeError("must specify how")


def isin(
    df: pd.DataFrame,
    values: Iterable | SeriesOrFrame | dict[str, list[str]],
    axis: IntOrStr = 0,
) -> pd.DataFrame:
    """
    Extend :meth:`~pandas.DataFrame.isin` function. When ``values`` is
    :obj:`dict` and ``axis`` is 1, ``values``' key could be index name.
    """
    from collections import defaultdict

    axis = df._get_axis_number(axis)

    if isinstance(values, dict) and axis == 1:
        values = defaultdict(list, values)
        result = (df.iloc[[r]].isin(values[i]) for r, i in enumerate(df.index))
        return pd.concat(result, axis=0)

    return df.isin(values)


# based on more_itertools/more.py
def collapse(iterable: Iterable):
    def walk(node):
        if isinstance(node, (str, bytes)):
            yield node
            return

        try:
            tree = iter(node)
        except TypeError:
            yield node
            return
        else:
            for child in tree:
                yield from walk(child)

    yield from walk(iterable)
