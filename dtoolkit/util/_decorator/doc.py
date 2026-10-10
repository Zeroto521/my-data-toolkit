from textwrap import dedent


# based on pandas.util._decorators.doc
def doc(*docstrings, **params):
    """
    A decorator to take docstring templates, concatenate them and perform string
    substitution on them.

    Parameters
    ----------
    *docstrings : None, str, or callable
        The string / docstring / docstring template to be appended in order
        after default docstring under callable.

    **params
        The string which would be used to format docstring template.

    Examples
    --------
    >>> from dtoolkit.util._decorator import doc

    >>> @doc(klass=":class:`~pandas.Series`")
    ... def method(s):
    ...     '''
    ...     {klass} method.
    ...     '''
    ...     pass
    ...
    >>> method.__doc__
    '\\n:class:`~pandas.Series` method.\\n'
    """

    def decorator(decorated):
        docstring_components: list[str] = []

        if decorated.__doc__:
            docstring_components.append(dedent(decorated.__doc__))

        for docstring in docstrings:
            if docstring is None:
                continue
            if hasattr(docstring, "_docstring_components"):
                docstring_components.extend(
                    docstring._docstring_components,
                )
            elif isinstance(docstring, str) or getattr(docstring, "__doc__", None):
                docstring_components.append(
                    docstring
                    if isinstance(docstring, str)
                    else dedent(docstring.__doc__),
                )

        decorated._docstring_components = docstring_components

        if len(params) > 0:
            docstring_components = [
                component.format(**params) if isinstance(component, str) else component
                for component in docstring_components
            ]

        decorated.__doc__ = "".join(docstring_components)
        return decorated

    return decorator
