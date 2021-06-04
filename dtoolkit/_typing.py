from __future__ import annotations

from typing import Any, Callable, TypeVar, Union

from pandas import DataFrame, Series

PandasType = Union[Series, DataFrame]
Pd = TypeVar("Pd", bound=PandasType)

FuncType = Callable[..., Any]
F = TypeVar("F", bound=FuncType)
