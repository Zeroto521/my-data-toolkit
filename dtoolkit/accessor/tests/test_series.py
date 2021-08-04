import pytest

from . import s, s_inf


class TestDropinfSeriesAccessor:
    def setup_method(self):
        self.s = s.copy(True)
        self.s = self.s.append(s_inf)

    @pytest.mark.parametrize(
        "df, expt",
        [
            (s, s),
            (s.append(s_inf), s),
        ],
    )
    def test_work(self, df, expt):
        res = df.dropinf()

        assert res.equals(expt)

    def test_inplace_is_true(self):
        res = self.s.dropinf(inplace=True)

        assert res is None
        assert self.s.equals(s)
