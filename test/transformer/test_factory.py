from __future__ import annotations

import numpy as np
import pytest

from dtoolkit.transformer.factory import methodtf_factory


def plus_constant(X: np.ndarray, constant: int | float) -> np.ndarray:
    return X + constant


def minus_constant(X: np.ndarray, constant: int | float) -> np.ndarray:
    return X - constant


class TestMethodtfFactory:
    @pytest.mark.parametrize(
        "data, method, inv_method, kwargs, inv_kwargs, excepted, inv_expt",
        [
            (
                # test transform method and inverse transfor method both have
                np.asarray([1, 2, 3]),
                plus_constant,
                minus_constant,
                dict(constant=1),
                dict(constant=0),
                np.asarray([2, 3, 4]),
                np.asarray([2, 3, 4]),
            ),
            (
                # test only transform method have
                np.asarray([1, 2, 3]),
                plus_constant,
                None,
                dict(constant=1),
                None,
                np.asarray([2, 3, 4]),
                np.asarray([2, 3, 4]),
            ),
        ],
    )
    def test_methodtf_factory(
        self,
        data,
        method,
        inv_method,
        kwargs,
        inv_kwargs,
        excepted,
        inv_expt,
    ):
        TF = methodtf_factory(method, inv_method)
        tf = TF(**(kwargs or ())).update_invargs(**(inv_kwargs or {}))

        transformed_data = tf.transform(data)
        inverse_data = tf.inverse_transform(transformed_data)

        assert "TF" in TF.__name__
        assert np.all(transformed_data == excepted)
        assert np.all(inverse_data == inv_expt)

    @pytest.mark.parametrize(
        "error, method, inv_method",
        [
            (TypeError, 1, None),
            (TypeError, lambda x: x, 1),
        ],
    )
    def test_error(self, error, method, inv_method):
        with pytest.raises(error):
            methodtf_factory(method, inv_method)
