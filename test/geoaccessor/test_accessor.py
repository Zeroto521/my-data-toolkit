import warnings
from contextlib import contextmanager
from contextlib import suppress

import geopandas as gpd
import pytest

from dtoolkit.geoaccessor.accessor import register_geodataframe_accessor
from dtoolkit.geoaccessor.accessor import register_geoseries_accessor

my_wkts = [
    "POINT (1 1)",
    "POINT (2 2)",
    "POINT (3 3)",
]


@contextmanager
def ensure_removed(obj, attr):
    """
    Ensure that an attribute added to 'obj' during the test is removed when we're done.
    """
    try:
        yield
    finally:
        with suppress(AttributeError):
            delattr(obj, attr)
        obj._accessors.discard(attr)


class MyAccessor:
    def __init__(self, obj):
        self.obj = obj
        self.item = "item"

    @property
    def prop(self):
        return self.item

    def method(self):
        return self.item


@pytest.mark.parametrize(
    "obj, registrar",
    [
        (gpd.GeoSeries, register_geoseries_accessor),
        (gpd.GeoDataFrame, register_geodataframe_accessor),
    ],
)
def test_register(obj, registrar):
    with ensure_removed(obj, "mine"):
        before = set(dir(obj))
        registrar("mine")(MyAccessor)
        o = obj([]) if obj is not gpd.GeoSeries else obj([], dtype=object)
        assert o.mine.prop == "item"
        after = set(dir(obj))
        assert (before ^ after) == {"mine"}
        assert "mine" in obj._accessors


def test_accessor_works():
    with ensure_removed(gpd.GeoSeries, "mine"):
        register_geoseries_accessor("mine")(MyAccessor)
        s = gpd.GeoSeries.from_wkt(my_wkts)

        assert s.mine.obj is s
        assert s.mine.prop == "item"
        assert s.mine.method() == "item"


def test_overwrite_warns():
    area = gpd.GeoSeries.area  # Need to restore

    try:
        with warnings.catch_warnings(record=True) as w:
            register_geoseries_accessor("area")(MyAccessor)
            s = gpd.GeoSeries.from_wkt(my_wkts)
            assert s.area.prop == "item"

        msg = str(w[0].message)

        assert "area" in msg
        assert "MyAccessor" in msg
        assert "GeoSeries" in msg

    finally:
        gpd.GeoSeries.area = area


def test_raises_attribute_error():
    with ensure_removed(gpd.GeoSeries, "bad"):

        @register_geoseries_accessor("bad")
        class Bad:
            def __init__(self, _):
                raise AttributeError("whoops")

        with pytest.raises(AttributeError, match="whoops"):
            gpd.GeoSeries([], dtype=object).bad
