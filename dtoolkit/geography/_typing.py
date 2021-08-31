from typing import Union

from geopandas import GeoDataFrame
from geopandas import GeoSeries


GeoPandasList = [GeoSeries, GeoDataFrame]
GeoPandasType = Union[tuple(GeoPandasList)]
