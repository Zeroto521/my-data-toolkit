import geopandas as gpd

from dtoolkit.geoaccessor.geodataframe import reverse_geocode


def test_type():
    df = pd.Series(
        [
            "POINT (-71.0594869 42.3584697)",
            "POINT (-77.0365305 38.8977332)",
        ],
    ).from_wkt(crs=4326)
    result = df.reverse_geocode()

    assert isinstance(df, gpd.GeoDataFrame)
