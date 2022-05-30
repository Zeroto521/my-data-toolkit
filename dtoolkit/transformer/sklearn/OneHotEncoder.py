from __future__ import annotations

from textwrap import dedent
from typing import TYPE_CHECKING

import pandas as pd
from pandas.util._decorators import doc
from sklearn.preprocessing import OneHotEncoder as SKOneHotEncoder

from dtoolkit._typing import TwoDimArray
from dtoolkit.accessor.dataframe import cols  # noqa
from dtoolkit.accessor.series import cols  # noqa

if TYPE_CHECKING:
    from scipy.sparse import csr_matrix


class OneHotEncoder(SKOneHotEncoder):
    """
    Encode categorical features as a one-hot numeric array.

    Parameters
    ----------
    categories_with_parent : bool, default False
        Returned column would hook parent labels if ``True`` else
        would be ``categories``.

    sparse : bool, default False
        Will return sparse matrix if ``True`` else will return an array.

    kwargs
        See :obj:`sklearn.preprocessing.OneHotEncoder`.

    Notes
    -----
    Different to :obj:`sklearn.preprocessing.OneHotEncoder`.
    The result would return a :obj:`~pandas.DataFrame` which uses categories
    as columns.

    Examples
    --------
    Given a dataset with two features, we let the encoder find the unique
    values per feature and transform the data to a binary one-hot encoding.

    :obj:`~pandas.DataFrame` in, :obj:`~pandas.DataFrame` out with categories
    as columns.

    >>> from dtoolkit.transformer import OneHotEncoder
    >>> import pandas as pd
    >>> X = [['Male', 1], ['Female', 3], ['Female', 2]]
    >>> df = pd.DataFrame(X, columns=['gender', 'number'])
    >>> df
        gender  number
    0    Male       1
    1  Female       3
    2  Female       2
    >>> enc = OneHotEncoder()
    >>> enc.fit_transform(df)
       Female  Male    1    2    3
    0     0.0   1.0  1.0  0.0  0.0
    1     1.0   0.0  0.0  0.0  1.0
    2     1.0   0.0  0.0  1.0  0.0

    The encoded data also could hook parent labels.

    >>> enc = OneHotEncoder(categories_with_parent=True)
    >>> enc.fit_transform(df)
       gender_Female  gender_Male  number_1  number_2  number_3
    0            0.0          1.0       1.0       0.0       0.0
    1            1.0          0.0       0.0       0.0       1.0
    2            1.0          0.0       0.0       1.0       0.0
    """

    @doc(SKOneHotEncoder.__init__)
    def __init__(
        self,
        categories_with_parent: bool = False,
        sparse: bool = False,
        **kwargs,
    ):
        super().__init__(sparse=sparse, **kwargs)
        self.categories_with_parent = categories_with_parent

    @doc(
        SKOneHotEncoder.transform,
        dedent(
            """
        Notes
        -----
        This would let :obj:`~pandas.DataFrame` out.
        """,
        ),
    )
    def transform(self, X: TwoDimArray) -> TwoDimArray | csr_matrix:
        from itertools import chain

        Xt = super().transform(X)

        if self.sparse is False and isinstance(X, (pd.Series, pd.DataFrame)):
            categories = (
                self.get_feature_names_out(X.cols(to_list=True))
                if self.categories_with_parent
                else chain.from_iterable(self.categories_)
            )

            return pd.DataFrame(Xt, columns=categories, index=X.index)

        return Xt
