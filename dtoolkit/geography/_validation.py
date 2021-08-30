from shapely.geometry.base import BaseGeometry

from .._typing import NumericType
from .._typing import NumericTypeList
from ..util._validation import istype
from ._typing import GeoPandasList
from ._typing import GPd


def check_geopandas_type(df: GPd):
    if not istype(df, GeoPandasList):
        raise TypeError(
            f"{df} must be GeoSeries or GeoDataFrame.",
        )


def check_geometry_type(geom: BaseGeometry):
    if not istype(geom, BaseGeometry):
        raise TypeError(
            f"{geom} must be Geometry.",
        )


def check_number_tyep(num: NumericType):
    if not istype(num, NumericTypeList):
        raise TypeError(
            f"The type of {num} must be int or float.",
        )


def check_greater_than_zero(num: NumericType):
    if num <= 0:
        raise ValueError(
            f"The {num} must be greater than 0.",
        )
