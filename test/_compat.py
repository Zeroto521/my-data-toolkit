# -----------------------------------------------------------------------------
# geopandas compat
# -----------------------------------------------------------------------------

HAS_GEOPANDAS = None

try:
    import geopandas  # noqa: F401

    HAS_GEOPANDAS = True

except ImportError:
    HAS_GEOPANDAS = False
