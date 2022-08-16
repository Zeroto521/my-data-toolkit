import geopandas as gpd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.accessor import register_geoseries_accessor


def tesspy_doc_decorator(func):
    """
    Wraps tesspy method docstring.

    Can't directly use `pandas.util._decorators.doc` to wraps dtoolkit's method.
    `tesspy` is a optional package for dtoolkit. We don't want to raise ImportError
    while doing `import dtoolkit.geoaccessor` without installing tesspy.
    """

    try:
        from tesspy import Tessellation as Tess

        return doc(getattr(Tess, func.__name__))(func)

    except ImportError:
        ...

    return func


@register_geoseries_accessor("tess")
@doc(klass="GeoSeries")
class Tessellation:
    """
    Tessellation for {klass}.

    Use this geoaccessor via
    ``{klass}.tess.(squares|hexagons|adaptive_squares|voronoi|city_blocks)``.

    Parameters
    *args, **kwargs
        Arguments passed to ``tesspy.Tessellation.{{method}}``.

    Returns
    -------
    GeoDataFrame
        Single column geometry.

    See Also
    --------
    tesspy.tessellation
    dtoolkit.geoaccessor.geoseries.Tessellation
    dtoolkit.geoaccessor.geodataframe.Tessellation
    """

    def __init__(self, s: gpd.GeoSeries):
        from tesspy import Tessellation as Tess

        self.tess = Tess(s.to_frame("geometry"))

    @tesspy_doc_decorator
    def squares(self, *args, **kwargs) -> gpd.GeoDataFrame:
        df = self.tess.squares(*args, **kwargs)
        return df[[df.geometry.name]].rename_geometry("geometry")

    @tesspy_doc_decorator
    def hexagons(self, *args, **kwargs) -> gpd.GeoDataFrame:
        df = self.tess.hexagons(*args, **kwargs)
        return df[[df.geometry.name]].rename_geometry("geometry")

    @tesspy_doc_decorator
    def adaptive_squares(self, *args, **kwargs) -> gpd.GeoDataFrame:
        df = self.tess.adaptive_squares(*args, **kwargs)
        return df[[df.geometry.name]].rename_geometry("geometry")

    @tesspy_doc_decorator
    def voronoi(self, *args, **kwargs) -> gpd.GeoDataFrame:
        df = self.tess.voronoi(*args, **kwargs)
        return df[[df.geometry.name]].rename_geometry("geometry")

    @tesspy_doc_decorator
    def city_blocks(self, *args, **kwargs) -> gpd.GeoDataFrame:
        df = self.tess.city_blocks(*args, **kwargs)
        return df[[df.geometry.name]].rename_geometry("geometry")
