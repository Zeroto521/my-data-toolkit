from __future__ import annotations

from pyproj import CRS
from pyproj import Transformer
from pyproj.crs import ProjectedCRS
from pyproj.crs.coordinate_operation import AzumuthalEquidistantConversion
from shapely.geometry import Point
from shapely.geometry.base import BaseGeometry
from shapely.ops import transform

from dtoolkit.geoaccessor._util import is_int_or_float
from dtoolkit.geoaccessor._util import string_or_int_to_crs


def geographic_buffer(
    geometry: BaseGeometry | None,
    distance: int | float,
    crs: CRS | None = None,
    **kwargs,
) -> BaseGeometry | None:
    """
    The core algorithm for creating a geographic buffer.

    Only support `Point` geometry, at present.

    .. warning::
        This method is deprecated and will be removed in 0.0.8. Please use
        :meth:`~dtoolkit.geoaccessor.geoseries.geobuffer` instead. (Warning added
        DToolKit 0.0.7)

    Parameters
    ----------
    geometry : Geometry or None
        Shapely geometry type, if the input is None, would be returned None also.

    distance : int or float
        The radius of buffer.

    crs : CRS or None
        if the input is None, would use the default CRS (EPSG:4326).

    Returns
    -------
    Geometry or None

    See Also
    --------
    dtoolkit.geoaccessor.geoseries.geobuffer
        Creates geographic buffers for GeoSeries.
    dtoolkit.geoaccessor.geodataframe.geobuffer
        Creates geographic buffers for GeoDataFrame.
    shapely.geometry.base.BaseGeometry.buffer
        https://shapely.readthedocs.io/en/latest/manual.html#object.buffer
    """

    if geometry is None:
        return None
    elif not isinstance(geometry, BaseGeometry):
        raise TypeError(f"{geometry} must be Geometry.")
    elif not isinstance(geometry, Point):
        # Only support 'Point' type to generate geographic buffer.
        return geometry

    if not is_int_or_float(distance):
        raise TypeError("The type of 'distance' must be int or float.")
    if distance <= 0:
        raise ValueError("The distance must be greater than 0.")

    crs = crs or string_or_int_to_crs()

    azmed = ProjectedCRS(AzumuthalEquidistantConversion(geometry.y, geometry.x))
    project: Transformer = Transformer.from_proj(azmed, crs, always_xy=True)

    # TODO: extend to other geometry
    buffer: BaseGeometry = Point(0, 0).buffer(distance, **kwargs)
    return transform(project.transform, buffer)
