from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from typing import Iterable


def get_inf_range(inf: str = "all") -> list[float]:
    inf_range = {
        "all": [np.inf, -np.inf],
        "pos": [np.inf],
        "+": [np.inf],
        "neg": [-np.inf],
        "-": [-np.inf],
    }

    if inf in inf_range:
        return inf_range[inf]

    raise ValueError(f"invalid inf option: {inf!r}")


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
