import geopandas as gpd
from dtoolkit.geoaccessor.accessor import register_geoseries_accessor


def tesspy_doc_decorator(func):
    """
    Wraps tesspy method docstring.

    Can't directly use `pandas.util._decorators.doc` to wraps dtoolkit's method.
    `tesspy` is a optional package for dtoolkit. We don't want to raise ImportError
    while doing `import dtoolkit.geoaccessor` without installing tesspy.
    """

    try:
        from pandas.util._decorators import doc
        from tesspy import Tessellation as Tess

        return doc(getattr(Tess, func.__name__))(func)

    except ImportError:
        ...

    return func


@register_geoseries_accessor("tess")
class Tessellation:
    def __init__(self, s: gpd.GeoSeries):
        from tesspy import Tessellation as Tess

        self.tess = Tess(s.to_frame("geometry"))

    @tesspy_doc_decorator
    def squares(self, *args, **kwargs) -> gpd.GeoDataFrame:
        return self.tess.squares(*args, **kwargs)

    @tesspy_doc_decorator
    def hexagons(self, *args, **kwargs) -> gpd.GeoDataFrame:
        return self.tess.hexagons(*args, **kwargs)

    @tesspy_doc_decorator
    def adaptive_squares(self, *args, **kwargs) -> gpd.GeoDataFrame:
        return self.tess.adaptive_squares(*args, **kwargs)

    @tesspy_doc_decorator
    def voronoi(self, *args, **kwargs) -> gpd.GeoDataFrame:
        return self.tess.voronoi(*args, **kwargs)

    @tesspy_doc_decorator()
    def city_blocks(self, *args, **kwargs) -> gpd.GeoDataFrame:
        return self.tess.city_blocks(*args, **kwargs)
