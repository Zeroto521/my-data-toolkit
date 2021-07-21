from __future__ import annotations

from typing import Any

from pandas import DataFrame
from shapely.geometry.base import BaseGeometry

from ._typing import GeoPandasList
from ._typing import GPd
from ._typing import NumericType
from ._typing import NumericTypeList


def istype(var: Any, types: type | list[type] | tuple[type]) -> bool:
    types: tuple[type] = containerize(types, tuple)

    return isinstance(var, types)


def containerize(var: Any, finaltype=list) -> list[Any] | tuple[Any]:
    if not isinstance(var, (list, tuple)):
        var = [var]

    return finaltype(var)


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
        not istype(geom, BaseGeometry),
        TypeError,
        f"{geom} must be Geometry.",
    )


def check_number_tyep(num: NumericType):
    bad_condition_raise_error(
        not istype(num, NumericTypeList),
        TypeError,
        f"The type of {num} must be int or float.",
    )


def check_greater_than_zero(num: NumericType):
    bad_condition_raise_error(
        num <= 0,
        ValueError,
        f"The {num} must be greater than 0.",
    )


def check_dataframe_type(df: DataFrame):
    bad_condition_raise_error(
        not isinstance(df, DataFrame),
        TypeError,
        "The input is not a 'DataFrame' type.",
    )
