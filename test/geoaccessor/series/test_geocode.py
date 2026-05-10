import importlib
from types import SimpleNamespace

import pandas as pd
import pytest

from dtoolkit.geoaccessor.series import geocode


pytest.importorskip("geopy")


@pytest.mark.parametrize(
    "s, drop, error",
    [
        (
            pd.Series(
                [
                    "boston, ma",
                    "1600 pennsylvania ave. washington, dc",
                ],
            ),
            False,
            ValueError,
        ),
    ],
)
def test_error(s, drop, error):
    with pytest.raises(error):
        geocode(s, drop=drop)


def test_geocode_stable_output(monkeypatch):
    module = importlib.import_module("dtoolkit.geoaccessor.series.geocode")

    def fake_geolocator(*args, **kwargs):
        return lambda address: SimpleNamespace(longitude=-71.05783, latitude=42.35883)

    monkeypatch.setattr(module, "geolocator", fake_geolocator)

    result = geocode(pd.Series(["boston, ma"], name="address"))

    assert "address" in result.columns
    assert "geometry" in result.columns
    assert result.loc[0, "address"] == "boston, ma"
    assert result.geometry.iloc[0].geom_type == "Point"
