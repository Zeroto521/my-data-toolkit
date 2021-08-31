import pytest

import dtoolkit._compat as compat

need_dependency = pytest.mark.skipif(
    not compat.HAS_GEOPANDAS,
    reason="geography need `geopandas`",
)
