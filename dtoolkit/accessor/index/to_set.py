import pandas as pd

from dtoolkit.accessor.register import register_index_method


@register_index_method
def to_set(index: pd.Index) -> set:
    """
    Return a :keyword:`set` of the values.

    A sugary syntax wraps :keyword:`set`::

        set(index)

    Different to :meth:`~pandas.Index.unique`, it returns :class:`~pandas.Index`.

    Returns
    -------
    set

    See Also
    --------
    pandas.Index.unique

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> i = pd.Index(["a", "b", "b"])
    >>> i
    Index(['a', 'b', 'b'], dtype='object')
    >>> i.to_set()
    {'a', 'b'}
    """

    return set(index)
