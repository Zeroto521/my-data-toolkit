from dtoolkit.util._decorator import warning


@warning(
    "'dtoolkit.util.generic.snake_to_camel' will be moved into "
    "'dtoolkit.transformer._util.snake_to_camel' as a inner function in 0.0.16. "
    "(Warning added DToolKit 0.0.15)",
    FutureWarning,
)
def snake_to_camel(name: str) -> str:
    """
    Change snake style name to camel style name.

    .. deprecated:: 0.0.15
        ``dtoolkit.util.generic.snake_to_camel`` will be moved into
        ``dtoolkit.transformer._util.snake_to_camel`` as a inner function in 0.0.16.
        (Warning added DToolKit 0.0.15)

    Parameters
    ----------
    name : str
        Snake style name

    Returns
    -------
    str
        Camel style name

    Examples
    --------
    >>> from dtoolkit.util import snake_to_camel
    >>> snake_to_camel(snake_to_camel.__name__)
    'SnakeToCamel'
    """

    components = name.split("_")
    components = (x.title() for x in components)
    return "".join(components)
