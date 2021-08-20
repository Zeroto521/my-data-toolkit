import numpy as np
import pytest

from dtoolkit.util import multi_if_else
from dtoolkit.util import wraps


class TestMultiIfElse:
    def setup_method(self):
        array = np.asarray(
            [
                [1, 0],
                [0, 1],
            ],
        )
        mask = array == 0
        self.if_condition_return_lambda = lambda how: [
            (how == "any", mask.any()),
            (how == "all", mask.all()),
            (how is not None, ValueError(f"Invalid how option: {how}")),
        ]

    @pytest.mark.parametrize(
        "how, expected",
        [
            ("any", True),
            ("all", False),
            (None, None),
        ],
    )
    def test_work(self, how, expected):
        if_condition_return = self.if_condition_return_lambda(how)
        res = multi_if_else(if_condition_return=if_condition_return)

        assert res == expected

    @pytest.mark.parametrize(
        "how, else_return, error",
        [
            ("whatevery", None, ValueError),
            (None, TypeError("Must specify how"), TypeError),
        ],
    )
    def test_error(self, how, else_return, error):
        if_condition_return = self.if_condition_return_lambda(how)

        with pytest.raises(error):
            multi_if_else(
                if_condition_return,
                else_return,
            )


class TestWraps:
    def setup_method(self):
        def method():
            """Method's doc here."""
            ...

        self.method = method

    def test_function(self):
        @wraps(self.method)
        def whatevery():
            """whatevery"""
            ...

        assert self.method.__name__ == whatevery.__name__
        assert self.method.__doc__ == whatevery.__doc__

    def test_class(self):
        @wraps(self.method)
        class whatevery:
            """whatevery"""

            ...

        assert self.method.__name__ == whatevery.__name__
        assert self.method.__doc__ == whatevery.__doc__
