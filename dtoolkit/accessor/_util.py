from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from typing import Iterable


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
