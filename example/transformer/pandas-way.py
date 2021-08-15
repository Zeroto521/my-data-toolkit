import pandas as pd

# basic data
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
df = pd.DataFrame.from_dict(store_sale_dict)

# Set a series of feature name constants.
features_category = ["floor", "type"]
features_number = ["level", "area", "population", "score"]
features = features_category + features_number
label = ["sale"]

# Filter opendays' store less than 30 days.
# Because these samples are not normal stores.
df = df.query("opendays > 30")

# Filter `'Home'` store.
df = df[df["type"] != "Home"]

# Transform sale to daily sale.
df.eval("sale = sale / opendays", inplace=True)

# Transform population to entry store population.
df.eval("population = score / 10 * population", inplace=True)

# Split `df` to `df_x` and `y`and separately process them.
df_x = df[features]
y = df[label]


# Scale `y`.
from sklearn.preprocessing import MinMaxScaler

y_scaler = MinMaxScaler()

# Scaler handle a column as a unit
y = y.values.reshape(-1, 1)

y = y_scaler.fit_transform(y)

# The model always requires a 1d array otherwise would give a warning.
y = y.ravel()
print(y)

# Replace store types to ranking numbers.
df_x.replace({"normal": 1, "important": 2, "strategic": 3}, inplace=True)

# Encode categorical features.
from sklearn.preprocessing import OneHotEncoder

x_encoder = OneHotEncoder(sparse=False)
x_category = x_encoder.fit_transform(df_x[features_category])

# Scale number features.
x_scaler = MinMaxScaler()
x_scaler = x_scaler.fit_transform(df_x[features_number])

# Merge all features to one.
import numpy as np

x = np.hstack([x_scaler, x_category])
print(x)
