# -----------------------------------------------------------------------------
# geopandas compat
# -----------------------------------------------------------------------------

HAS_GEOPANDAS = None

try:
    import geopandas

    HAS_GEOPANDAS = True

except ImportError:
    HAS_GEOPANDAS = False
