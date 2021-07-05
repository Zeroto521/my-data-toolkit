from __future__ import annotations

from typing import List, Tuple

from pandas import DataFrame
from shapely.geometry.base import BaseGeometry

from ._typing import GeoPandasList, GPd, NumericType, NumericTypeList


def istype(var: object, types: type | List[type] | Tuple[type]) -> bool:
    if isinstance(types, list):
        types: Tuple[type] = tuple(types)

    return isinstance(var, types)


def bad_condition_raise_error(condition: bool, error: BaseException, msg: str):
    if condition:
        raise error(msg)


def check_geopandas_type(df: GPd):
    bad_condition_raise_error(
        not istype(df, GeoPandasList),
        TypeError,
        f"{df} must be GeoSeries or GeoDataFrame.",
    )


def check_geometry_type(geom: BaseGeometry):
    bad_condition_raise_error(
        not istype(geom, BaseGeometry), TypeError, f"{geom} must be Geometry."
    )


def check_number_tyep(num: NumericType):
    bad_condition_raise_error(
        not istype(num, NumericTypeList),
        TypeError,
        f"The type of {num} must be int or float.",
    )


def check_greater_than_zero(num: NumericType):
    bad_condition_raise_error(
        num <= 0, ValueError, f"The {num} must be greater than 0."
    )


def check_dataframe_type(df: DataFrame):
    bad_condition_raise_error(
        not isinstance(df, DataFrame),
        TypeError,
        "The input is not a 'DataFrame' type.",
    )
