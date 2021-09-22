from typing import Tuple
from typing import Union

import geopandas as gpd
from numpy import float32
from numpy import float64
from numpy import float_
from numpy import int16
from numpy import int32
from numpy import int64
from numpy import int8
from numpy import uint16
from numpy import uint32
from numpy import uint64
from numpy import uint8


GeoSeriesOrGeoFrame = Union[gpd.GeoSeries, gpd.GeoDataFrame]

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
