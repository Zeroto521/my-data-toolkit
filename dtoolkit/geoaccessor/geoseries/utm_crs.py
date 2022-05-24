import geopandas as gpd
import pandas as pd
from pyproj.aoi import AreaOfInterest
from pyproj.database import query_utm_crs_info

from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
def utm_crs(s: gpd.GeoSeries, datum_name: str = "WGS 84") -> pd.Series:
    """
    Returns the estimated UTM CRS based on the bounds of each geometry.

    Parameters
    ----------
    datum_name : str, default 'WGS 84'
        The name of the datum in the CRS name ('NAD27', 'NAD83', 'WGS 84', …).

    Returns
    -------
    Series
        The element type is :class:`~pyproj.database.CRSInfo`.

    See Also
    --------
    dtoolkit.geoaccessor.geoseries.utm_crs
        Returns the estimated UTM CRS based on the bounds of each geometry.
    dtoolkit.geoaccessor.geodataframe.utm_crs
        Returns the estimated UTM CRS based on the bounds of each geometry.
    geopandas.GeoSeries.estimate_utm_crs
        Returns the estimated UTM CRS based on the bounds of the dataset.
    geopandas.GeoDataFrame.estimate_utm_crs
        Returns the estimated UTM CRS based on the bounds of the dataset.

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import dtoolkit.geoaccessor
    >>> import geopandas as gpd
    >>> s = gpd.GeoSeries.from_wkt(["Point (120 50)", "Point (100 1)"], crs="epsg:4326")
    >>> s.utm_crs()
    0    (EPSG, 32650, WGS 84 / UTM zone 50N, PJType.PR...
    1    (EPSG, 32647, WGS 84 / UTM zone 47N, PJType.PR...
    dtype: object

    Same operate for GeoDataFrame.

    >>> s.to_frame("geometry").utm_crs()
    0    (EPSG, 32650, WGS 84 / UTM zone 50N, PJType.PR...
    1    (EPSG, 32647, WGS 84 / UTM zone 47N, PJType.PR...
    dtype: object

    Get the EPSG code.

    >>> s.utm_crs().getattr("code")
    0    32650
    1    32647
    dtype: object
    """

    return s.bounds.apply(
        lambda bound: None
        if bound.isna().all()
        else query_utm_crs_info(
            datum_name=datum_name,
            area_of_interest=AreaOfInterest(
                west_lon_degree=bound["minx"],
                south_lat_degree=bound["miny"],
                east_lon_degree=bound["maxx"],
                north_lat_degree=bound["maxy"],
            ),
        )[0],
        axis=1,
    )
