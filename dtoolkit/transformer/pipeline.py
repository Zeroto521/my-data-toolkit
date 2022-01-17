from __future__ import annotations

import pandas as pd
from sklearn.pipeline import FeatureUnion as SKFeatureUnion
from dtoolkit.transformer.base import Transformer


class FeatureUnion(SKFeatureUnion, Transformer):
    """
    Concatenates results of multiple transformer objects.

    See Also
    --------
    make_union
        Convenience function for simplified feature union construction.

    Notes
    -----
    Different to :obj:`sklearn.pipeline.FeatureUnion`.
    This would let :obj:`~pandas.DataFrame` in and
    :obj:`~pandas.DataFrame` out.

    Examples
    --------
    >>> from dtoolkit.transformer import FeatureUnion
    >>> from sklearn.decomposition import PCA, TruncatedSVD
    >>> union = FeatureUnion([("pca", PCA(n_components=1)),
    ...                       ("svd", TruncatedSVD(n_components=2))])
    >>> X = [[0., 1., 3], [2., 2., 5]]
    >>> union.fit_transform(X)
    array([[ 1.5       ,  3.0...,  0.8...],
           [-1.5       ,  5.7..., -0.4...]])
    """

    def _hstack(self, Xs):
        if all(isinstance(i, (pd.Series, pd.DataFrame)) for i in Xs):
            Xs = (i.reset_index(drop=True) for i in Xs)
            return pd.concat(Xs, axis=1)

        return super()._hstack(Xs)


def make_union(
    *transformers: list[Transformer],
    n_jobs: int | None = None,
    verbose: bool = False,
) -> FeatureUnion:
    """
    Construct a FeatureUnion from the given transformers.

    See Also
    --------
    FeatureUnion
        Class for concatenating the results of multiple transformer objects.

    Notes
    -----
    Different to :obj:`sklearn.pipeline.make_union`.
    This would let :obj:`~pandas.DataFrame` in and
    :obj:`~pandas.DataFrame` out.

    Examples
    --------
    >>> from sklearn.decomposition import PCA, TruncatedSVD
    >>> from dtoolkit.transformer import make_union
    >>> make_union(PCA(), TruncatedSVD())
     FeatureUnion(transformer_list=[('pca', PCA()),
                                   ('truncatedsvd', TruncatedSVD())])
    """
    from sklearn.pipeline import _name_estimators

    return FeatureUnion(
        _name_estimators(transformers),
        n_jobs=n_jobs,
        verbose=verbose,
    )
