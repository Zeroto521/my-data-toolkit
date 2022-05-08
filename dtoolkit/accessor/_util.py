from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

from dtoolkit.util import multi_if_else

if TYPE_CHECKING:
    from typing import Iterable

    from dtoolkit._typing import IntOrStr
    from dtoolkit._typing import OneDimArray
    from dtoolkit._typing import SeriesOrFrame
    from dtoolkit._typing import TwoDimArray


def get_inf_range(inf: str = "all") -> list[float]:
    return multi_if_else(
        [
            (inf == "all", [np.inf, -np.inf]),
            (inf == "pos", [np.inf]),
            (inf == "neg", [-np.inf]),
            (inf is not None, ValueError(f"invalid inf option: {inf!r}")),
        ],
        TypeError("must specify 'inf'"),
    )


def get_mask(how: str, mask: TwoDimArray, axis: int) -> OneDimArray:
    return multi_if_else(
        [
            (how == "any", mask.any(axis=axis)),
            (how == "all", mask.all(axis=axis)),
            (how is not None, ValueError(f"invalid inf option: {how!r}")),
        ],
        TypeError("must specify 'how'"),
    )


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
