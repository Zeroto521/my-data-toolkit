from __future__ import annotations

from typing import TypeVar, Union

from pandas import DataFrame, Series

PandasType = Union[Series, DataFrame]
Pd = TypeVar("Pd", bound=PandasType)

