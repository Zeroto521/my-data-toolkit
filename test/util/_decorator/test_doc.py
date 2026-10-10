from dtoolkit.util._decorator import doc


def test_basic_params():
    @doc(klass="Series")
    def func():
        """{klass} method."""

    assert "Series method" in func.__doc__


def test_multiple_params():
    @doc(alias="s", klass="Series")
    def func():
        """{alias} = {klass}()"""

    assert "s = Series()" in func.__doc__


def test_no_params():
    @doc()
    def func():
        """Hello world."""

    assert "Hello world" in func.__doc__


def test_no_docstring():
    @doc(klass="Series")
    def func():
        pass

    assert func.__doc__ is None


def test_none_docstring():
    @doc(None, klass="Series")
    def func():
        """{klass} method."""

    assert "Series method" in func.__doc__


def test_string_docstring():
    @doc("Appended text.", klass="Series")
    def func():
        """{klass} method."""

    assert "Series method" in func.__doc__
    assert "Appended text." in func.__doc__


def test_inherit_docstring():
    def source():
        """Source docstring."""

    @doc(source, klass="Series")
    def func():
        """{klass} method."""

    assert "Series method" in func.__doc__
    assert "Source docstring." in func.__doc__


def test_chained_decorators():
    def source():
        """{klass} source."""

    source = doc(klass="Source")(source)

    @doc(source, klass="Derived")
    def func():
        """{klass} derived."""

    assert "Derived derived" in func.__doc__
    assert "Source source" in func.__doc__


def test_chained_formatter_not_reformatted():
    def source():
        """{klass} source."""

    source = doc(klass="Source")(source)

    @doc(source)
    def func():
        """{klass} derived."""

    assert "Source source" in func.__doc__
    assert "{klass} derived" in func.__doc__


def test_docstring_components_tracked():
    @doc(klass="Series")
    def func():
        """{klass} method."""

    assert hasattr(func, "_docstring_components")
    assert isinstance(func._docstring_components, list)


def test_inherit_multiple_sources():
    def source1():
        """First source."""

    def source2():
        """Second source."""

    @doc(source1, source2)
    def func():
        """Main doc."""

    assert "Main doc" in func.__doc__
    assert "First source" in func.__doc__
    assert "Second source" in func.__doc__


def test_dedent_applied():
    @doc(klass="Series")
    def func():
        """
        {klass} method.
        """

    assert "Series method" in func.__doc__
    assert "    Series method" not in func.__doc__


def test_original_pandas_style():
    @doc(klass=":class:`~pandas.Series`")
    def method(s):
        """
        {klass} method.
        """

    assert ":class:`~pandas.Series` method." in method.__doc__


def test_examples_param():
    examples = ">>> import pandas as pd"

    @doc(examples=examples, klass="Series")
    def func():
        """
        {klass} method.

        Examples
        --------
        {examples}
        """

    assert "Series method" in func.__doc__
    assert ">>> import pandas as pd" in func.__doc__
