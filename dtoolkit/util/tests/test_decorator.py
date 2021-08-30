from dtoolkit.util import wraps


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
