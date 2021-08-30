from shapely.geometry.base import BaseGeometry

from ..util._validation import istype
from ._typing import GeoPandasList
from ._typing import GPd


def check_geopandas_type(df: GPd):
    if not istype(df, GeoPandasList):
        raise TypeError(
            f"{df} must be GeoSeries or GeoDataFrame.",
        )


def check_geometry_type(geom: BaseGeometry):
    if not isinstance(geom, BaseGeometry):
        raise TypeError(
            f"{geom} must be Geometry.",
        )
