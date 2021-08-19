import numpy as np
import pandas as pd
import pytest

from . import s
from . import s_inf
from dtoolkit.accessor.series import dropinf  # noqa


class TestDropinf:
    def setup_method(self):
        self.s = s.copy(True)
        self.s = self.s.append(s_inf)

    @pytest.mark.parametrize(
        "inf, df, expt",
        [
            ("all", s, s),
            ("all", s.append(s_inf), s),
            ("pos", s_inf, pd.Series([-np.inf], index=[1])),
            ("neg", s_inf, pd.Series([np.inf])),
        ],
    )
    def test_work(self, inf, df, expt):
        res = df.dropinf(inf=inf)

        assert res.equals(expt)

    def test_inplace_is_true(self):
        res = self.s.dropinf(inplace=True)

        assert res is None
        assert self.s.equals(s)

    @pytest.mark.parametrize(
        "error, inf",
        [
            (ValueError, np.inf),
            (TypeError, None),
        ],
    )
    def test_error(self, error, inf):
        with pytest.raises(error):
            s_inf.dropinf(inf=inf)
