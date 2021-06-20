import geopandas as gpd
import pytest
from dtoolkit.coordinate import _coords, _coords_num, coords, coords_num, coords_numlist
from more_itertools import collapse
from shapely.geometry import (
    LinearRing,
    LineString,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
    Point,
    Polygon,
)

cpoint = [(100, 1)]
point = Point(cpoint)
cpoints = [(0, 0), (120, 50), (100, 1)]
points = MultiPoint(cpoints)

cline = [(0, 0), (1, 1)]
line = LineString(cline)
cring = [(0, 0), (1, 1), (1, 0)]
ring = LinearRing(cring)
clines = [((0, 0), (1, 1)), ((-1, 0), (1, 0))]
lines = MultiLineString(clines)

cpolygon = [(0, 0), (1, 1), (1, 0)]
polygon = Polygon(cpolygon)

_coords_a = [(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)]
_coords_b = [(1, 1), (1, 2), (2, 2), (2, 1), (1, 1)]
cmultipolygon = [[_coords_a, []], [_coords_b, []]]
multipolygon = MultiPolygon(cmultipolygon)

_cline_a = [(0, 0), (1, 1), (1, 2), (2, 2)]
_cline_b = [(0, 0), (1, 1), (2, 1), (2, 2)]
_line_a = LineString(_cline_a)
_line_b = LineString(_cline_b)
ccollections = [_cline_a, _cline_b]
collections = _line_a.intersection(_line_b)

cgeometrys = [
    cpoint,
    cpoints,
    cline,
    cring,
    clines,
    cpolygon,
    cmultipolygon,
    ccollections,
]

geometrys = [
    point,
    points,
    line,
    ring,
    lines,
    polygon,
    multipolygon,
    collections,
]


@pytest.mark.parametrize("rcoord,geom", zip(cgeometrys, geometrys))
def test_single_geometry_coords(rcoord, geom):
    tcoord = _coords(geom)

    tcoord = unique_point(tcoord)
    rcoord = unique_point(rcoord)

    assert tcoord == rcoord


def test_none_geometry_coords():
    with pytest.raises(TypeError):
        _coords(None)


def test_geoseries_coords():
    s = gpd.GeoSeries(geometrys)

    tcoords = coords(s)
    for tcoord, rcoord in zip(tcoords, cgeometrys):
        tcoord = unique_point(tcoord)
        rcoord = unique_point(rcoord)

        assert tcoord == rcoord


def test_not_geopandas_coords():
    with pytest.raises(TypeError):
        coords(None)


def unique_point(coords):
    return set(collapse(coords, levels=2))


@pytest.mark.parametrize("geom", (geometrys))
def test_single_geometry_coords_num(geom):
    _coords_num(geom)


def test_geoseries_coords_num():
    s = gpd.GeoSeries(geometrys)
    coords_num(s)

def test_not_geopandas_coords_num():
    with pytest.raises(TypeError):
        coords_num(None)

def test_geoseries_coords_numlist():
    s = gpd.GeoSeries(geometrys)
    coords_numlist(s)

