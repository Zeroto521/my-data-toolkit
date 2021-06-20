from typing import Tuple, TypeVar, Union

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


#
# numeric type
#
NumericBaseList = [int, float]
NumericBaseType = Union[tuple(NumericBaseList)]

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

GeoPandasList = [GeoSeries, GeoDataFrame]
GeoPandasType = Union[tuple(GeoPandasList)]
GPd = TypeVar("GPd", bound=GeoPandasType)


#
# shapely geometry coordinate type
#
PointType = Tuple[NumericBaseType]

# this type could represent `LineString`, `LinearRing`
LineType = Tuple[PointType]

# this type also could represent `MultiLineString``
PolygonType = Tuple[LineType]

MultiPolygonType = Tuple[PolygonType]

CoordType = Union[PointType, LineType, PolygonType, MultiPolygonType]


CoordNumType = Union[int, Tuple[int], Tuple[Tuple[int]]]
