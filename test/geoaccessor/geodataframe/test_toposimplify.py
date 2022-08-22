import pytest

gpd = pytest.importorskip("geopandas")

from dtoolkit.geoaccessor.geodataframe import toposimplify  # noqa: F401


def test_type():
    df = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    result = df.toposimplify(0.1)

    assert isinstance(result, gpd.GeoDataFrame)
