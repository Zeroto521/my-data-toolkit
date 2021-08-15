import pandas as pd
from dtoolkit.transformer import (
    EvalTF,
    FilterInTF,
    GetTF,
    MinMaxScaler,
    OneHotEncoder,
    QueryTF,
    RavelTF,
    ReplaceTF,
    make_union,
)
from sklearn.pipeline import make_pipeline

store_sale_dict = {
    "code": ["811-10001", "811-10002", "811-10003", "811-10004"],
    "name": ["A", "B", "C", "D"],
    "floor": ["1F", "2F", "1F", "B2"],
    "level": ["important", "normal", "important", "normal"],
    "type": ["School", "Mall", "Office", "Home"],
    "area": [100, 95, 177, 70],
    "population": [3000, 1000, 2000, 1500],
    "score": [10, 8, 6, 5],
    "opendays": [300, 100, 250, 30],
    "sale": [8000, 5000, 3000, 1500],
}
df = pd.DataFrame(store_sale_dict)

features_category = ["floor", "type"]
features_number = ["level", "area", "population", "score"]
features = features_category + features_number
label = ["sale"]


pl_xy = make_pipeline(
    QueryTF("opendays > 30"),
    FilterInTF({"type": ["School", "Mall", "Office"]}),
    EvalTF("sale = sale / opendays"),
    EvalTF("population = score / 10 * population"),
)
pl_x = make_pipeline(
    GetTF(features),
    ReplaceTF({"normal": 1, "important": 2, "strategic": 3}),
    make_union(
        make_pipeline(
            GetTF(features_category),
            OneHotEncoder(),
        ),
        make_pipeline(
            GetTF(features_number),
            MinMaxScaler(),
        ),
    ),
)
pl_y = make_pipeline(
    GetTF(label),
    MinMaxScaler(),
    RavelTF(),
)


xy = pl_xy.fit_transform(df)
X = pl_x.fit_transform(xy)
y = pl_y.fit_transform(xy)

print(xy)
print(X)
print(y)
