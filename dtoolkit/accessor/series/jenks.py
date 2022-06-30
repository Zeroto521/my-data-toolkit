from __future__ import annotations

from typing import Hashable

import pandas as pd

from .bin import bin  # noqa
from pandas.api.extensions import register_series_accessor


@register_series_accessor("jenks")
class Jenks:
    def __init__(self, s: pd.Series):
        self.s = s

    def breaks(self, bins: int) -> tuple:
        from jenkspy import jenks_breaks

        return jenks_breaks(self.s, bins)

    def bin(self, bins: int, **kwargs) -> pd.Series:
        breaks = self.breaks(bins)
        labels = range(len(breaks)) if flag == "int" else None

        return self.s.bin(breaks, labels=labels, **kwargs)
