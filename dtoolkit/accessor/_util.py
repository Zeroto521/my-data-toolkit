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
