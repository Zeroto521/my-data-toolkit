import pandas as pd
import pytest
from dtoolkit.accessor import FilterInAccessor  # noqa
from dtoolkit.accessor import RepeatAccessor  # noqa

from . import d


class TestFilterInAccessor:
    def setup_method(self):
        self.d = d.copy(True)
        self.condition = {"a": [0, 1], "b": [2]}

    def test_work(self):
        res = self.d.filterin(self.condition)

        assert res["a"].isin([0, 1]).any()  # 0 and 1 in a
        assert (~res["a"].isin([2])).all()  # 2 not in a
        assert res["b"].isin([2]).any()  # 2 in a
        assert (~res["b"].isin([0, 1])).all()  # 0 and not in a

    def test_inplace_is_true(self):
        res = self.d.filterin(self.condition, inplace=True)

        assert res is None
        assert self.d.equals(d) is False


class TestRepeatAccessor:
    def setup_method(self):
        self.d = pd.DataFrame({"a": [1, 2], "b": [3, 4]})

    @pytest.mark.parametrize(
        "repeats, axis, expected",
        [
            (
                2,
                0,
                pd.DataFrame(
                    {
                        "a": [1, 1, 2, 2],
                        "b": [3, 3, 4, 4],
                    },
                    index=[0, 0, 1, 1],
                ),
            ),
            (
                2,
                1,
                pd.DataFrame(
                    [
                        [1, 1, 3, 3],
                        [2, 2, 4, 4],
                    ],
                    columns=["a", "a", "b", "b"],
                ),
            ),
            (
                [1, 2],
                1,
                pd.DataFrame(
                    [
                        [1, 3, 3],
                        [2, 4, 4],
                    ],
                    columns=["a", "b", "b"],
                ),
            ),
        ],
    )
    def test_work(self, repeats, axis, expected):
        result = self.d.repeat(repeats, axis)

        assert result.equals(expected)

    @pytest.mark.parametrize("axis", [-1, 3, None])
    def test_error(self, axis):
        with pytest.raises(ValueError):
            self.d.repeat(2, axis)
