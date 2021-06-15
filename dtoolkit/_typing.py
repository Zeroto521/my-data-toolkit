from __future__ import annotations

from typing import Any, TypeVar, Union

from geopandas import GeoDataFrame, GeoSeries
from numpy import (
    float32,
    float64,
    float_,
    int8,
    int16,
    int32,
    int64,
    uint8,
    uint16,
    uint32,
    uint64,
)
from pandas import DataFrame, Series

NumericBaseList = [int, float]
NumericNumpyList = [
    # int
    int8,
    int16,
    int32,
    int64,
    # uint
    uint8,
    uint16,
    uint32,
    uint64,
    # float
    float32,
    float64,
    float_,
]
NumericTypeList = NumericBaseList + NumericNumpyList
NumericType = Union[tuple(NumericTypeList)]
Num = TypeVar("Num", bound=NumericType)

PandasTypeList = [Series, DataFrame]
PandasType = Union[tuple(PandasTypeList)]
Pd = TypeVar("Pd", bound=PandasType)

GeoPandasType = Union[GeoSeries, GeoDataFrame]
GPd = TypeVar("GPd", bound=GeoPandasType)


def var_bad_type_raise_error(
    var: Any,
    types: list[object] | tuple[object],
    error: BaseException,
    message: str,
):
    if not isinstance(var, tuple(types)):
        raise error(message)
