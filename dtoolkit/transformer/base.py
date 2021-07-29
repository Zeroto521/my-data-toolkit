from sklearn.base import TransformerMixin


class Transformer(TransformerMixin):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def operate(self, X, *_, **__):
        return X

    def validate(self, *_, **__):
        ...

    def fit(self, *_):
        return self

    def transform(self, X, *_):
        self.validate(X)

        return self.operate(X, *self.args, **self.kwargs)

    def fit_transform(self, X, *_):
        return self.fit().transform(X)

    def inverse_transform(self, X, *_):
        return X
