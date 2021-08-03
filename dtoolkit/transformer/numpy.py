import numpy as np

from .base import Transformer


# RavelTF doc ported with modifications from pandas
# https://github.com/numpy/numpy/blob/main/numpy/core/fromnumeric.py


class RavelTF(Transformer):
    """
    Return a contiguous flattened array.

    Parameters
    ----------
    order : {'C','F', 'A', 'K'}, optional
        The elements of `a` (input data) are read using this index order.

        * 'C' means to index the elements in row-major, C-style order,
            with the last axis index changing fastest, back to the first
            axis index changing slowest.

        * 'F' means to index the elements in column-major, Fortran-style
            order, with the first index changing fastest, and the last index
            changing slowest. Note that the 'C' and 'F' options take no account
            of the memory layout of the underlying array, and only refer to
            the order of axis indexing.

        * 'A' means to read the elements in Fortran-like index order if
            `a` is Fortran *contiguous* in memory, C-like order otherwise.

        * 'K' means to read the elements in the order they occur in memory,
            except for reversing the data when strides are negative.

        By default, 'C' index order is used.

    Returns
    -------
    y : array_like
        y is an array of the same subtype as `a`, with shape ``(a.size,)``.
        Note that matrices are special cased for backward compatibility, if `a`
        is a matrix, then y is a 1-D ndarray.

    Notes
    -----
    In row-major, C-style order, in two dimensions, the row index
    varies the slowest, and the column index the quickest.  This can
    be generalized to multiple dimensions, where row-major order
    implies that the index along the first axis varies slowest, and
    the index along the last quickest.  The opposite holds for
    column-major, Fortran-style index ordering.

    When a view is desired in as many cases as possible, ``arr.reshape(-1)``
    may be preferable.

    See Also
    --------
    numpy.ravel : Similar method for :class:`numpy.ndarray`.

    Examples
    --------
    >>> from dtoolkit.transformer import RavelTF
    >>> x = np.array([[1, 2, 3], [4, 5, 6]])
    >>> tf = RavelTF()
    >>> tf.transform(x)
    array([1, 2, 3, 4, 5, 6])
    """

    def operate(self, *args, **kwargs):
        return np.ravel(*args, **kwargs)
