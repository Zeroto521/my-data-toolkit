from __future__ import annotations

from typing import TypeVar, Union

from geopandas import GeoDataFrame, GeoSeries
from pandas import DataFrame, Series

NumericType = Union[int, float]
Num = TypeVar("Num", bound=NumericType)

PandasType = Union[Series, DataFrame]
Pd = TypeVar("Pd", bound=PandasType)

GeoPandasType = Union[GeoSeries, GeoDataFrame]
GPd = TypeVar("GPd", bound=GeoPandasType)
