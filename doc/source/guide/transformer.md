# Transformer and Pipeline Quickstart

`Transformer` faces the engineering of **data preprocessing**.

## Applicable Scene

In steps of data preprocessing, we always need to do some **duplication things**.

When we finished dealing with the training dataset, we also need to sort those
preprocessing steps out and make them to a function, a API, or something.

## Sample Data

:::{note}
All data are virtual.
:::

There are some stores sale data of one chain brand.

- These stores place one region.
- Time is one specific year.
- Sale is a year total amount.
- Population is surrounding {math}`200m` buffer daily people numbers.
- Score is given by the expert, ranges from 0 to 10.

```{code-block} python
>>> import pandas as pd

>>> store_sale_dict = {
...     "code": ["811-10001", "811-10002", "811-10003", "811-10004"],
...     "name": ["A", "B", "C", "D"],
...     "floor": ["1F", "2F", "1F", "B2"],
...     "level": ["strategic", "normal", "important", "normal"],
...     "type": ["School", "Mall", "Office", "Home"],
...     "area": [100, 95, 177, 70],
...     "population": [3000, 1000, 2000, 1500],
...     "score": [10, 8, 6, 5],
...     "opendays": [300, 100, 250, 15],
...     "sale": [8000, 5000, 3000, 1500],
... }
>>> df = pd.DataFrame(store_sale_dict)
>>> df
        code name floor      level    type  area  population  score  opendays  sale
0  811-10001    A    1F  strategic  School   100        3000     10       300  8000
1  811-10002    B    2F     normal    Mall    95        1000      8       100  5000
2  811-10003    C    1F  important  Office   177        2000      6       250  3000
3  811-10004    D    B2     normal    Home    70        1500      5        15  1500
```

## Feature Types and Dealing Steps

First of all, we should konw there are three types of features ( {math}`X`) and one label ( {math}`y`).

- Additional information features: drop
  - code
  - name
- Categorical features: encode to one-hot
  - floor
  - type: drop `'Home'` type, this type store numbers are very small.
- Number features: scale
  - level: it is not **categorical** type, because it could be compared.
  - area
  - population: there is buffer ranging population, but more want to enter store population, equal to  {math}`\frac{score}{10} \times population`.
  - score
  - opendays: filter `opendays <= 30` stores then drop this field
- Label: need to balance, should transform to daily sale, equal to {math}`\frac{sale}{opendays}` then sacle

:::{admonition} Mission
Our mission is to find some relationships between these features and label.
:::

(the-pandas-way)=
## The Pandas Way

In pandas code, most users might type something like this:

Set a series of feature name constants.

```{code-block} python
features_category = ["floor", "type"]
features_number = ["level", "area", "population", "score"]
features = features_category + features_number
label = ["sale"]
```

### Process `X` and `y`

```{code-block} python
# Filter opendays' store less than 30 days.
# Because these samples are not normal stores.
df = df.query("opendays > 30")

# Filter `'Home'` store.
df = df[df["type"]!="Home"]

# Transform sale to daily sale.
df.eval('sale = sale / opendays', inplace=True)

# Transform population to entry store population.
df.eval('population = score / 10 * population', inplace=True)

# Split `df` to `df_x` and `y`and separately process them.
df_x = df[features]
y = df[label]
```

(process-y)=
### Process `y`

```{code-block} python
# Scale `y`.
from sklearn.preprocessing import MinMaxScaler

y_scaler = MinMaxScaler()

# Scaler handle a column as a unit
y = y.values.reshape(-1, 1)

y = y_scaler.fit_transform(y)

# The model always requires a 1d array otherwise would give a warning.
y = y.ravel()
```

Output `y`

```{code-block} python
>>> y
[0.38596491 1.         0.        ]
```

(process-X)=
### Process `X`

```{code-block} python
# Replace store types to ranking numbers.
df_x.replace({"normal": 1, "important": 2, "strategic": 3}, inplace=True)

# Encode categorical features.
from sklearn.preprocessing import OneHotEncoder

x_encoder = OneHotEncoder()
x_category = x_encoder.fit_transform(df_x[features_category])

# Scale number features.
x_scaler = MinMaxScaler()
x_scaler = x_scaler.fit_transform(df_x[features_number])

# Merge all features to one.
import numpy as np

X = np.stack([x_scaler, x_category])
```

Output `X`

```{code-block} python
>>> X
[[1.         0.06097561 1.         1.         1.         0.
  0.         0.         1.        ]
 [0.         0.         0.         0.5        0.         1.
  1.         0.         0.        ]
 [1.         1.         0.18181818 0.         1.         0.
  0.         1.         0.        ]]
```

## The Pipeline Way

From {ref}`the-pandas-way` section, we can see that:

- The intermediate variables are full of steps. We don't care about them atthe most time except debugging and reviewing.
- Data workflow is messy. Hard to separate data and operations.
- The outputting datastruct is not comfortable. The inputting type is {obj}`~pandas.DataFrame` but the outputting type is {obj}`~numpy.ndarray`.
- Hard to apply in prediction data.

(further-one-step-to-pipeline)=
### Further One Step to Pipeline

{obj}`~sklearn.pipeline.Pipeline` is a good frame to fix these problems.

Transform {ref}`process-x` and {ref}`process-y` section codes to pipeline codees.

But actually, these things are hard to transform to pipeline.
Most are pandas methods, only OneHotEncoder and MinMaxScaler is could be added
into {obj}`~sklearn.pipeline.Pipeline`.

The codes are still messy on **typing** and **applying** two ways.

## The {ref}`dtoolkit.transformer <transformer>` Way

Frame is good, but from {ref}`further-one-step-to-pipeline` section we could
see that the core problem is **missing transformer**.

- Pandas's methods couldn't be used as a transformer.
- Numpy's methods couldn't be used as a transformer.
- Sklearn's transformers can't pandas in and pandas out.

### Further More Steps to Pipeline

Data Workflow:

```{code-block} python
---
emphasize-lines: 16-19, 22-33, 36-38
---
from dtoolkit.transformer import (
    EvalTF,
    FilterInTF,
    GetTF,
    MinMaxScaler,
    ReplaceTF,
    OneHotEncoder,
    QueryTF,
    make_union,
    RavelTF,
)
from sklearn.pipeline import **make_pipeline**


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
```

Apply to data:

```{code-block} python
xy = pl_xy.fit_transform(df)
X = pl_x.fit_transform(xy)
y = pl_y.fit_transform(xy)
```

Output:

```{code-block} python
>>> xy
        code name floor      level    type  area  population  score  opendays       sale
0  811-10001    A    1F  important  School   100      3000.0     10       300  26.666667
1  811-10002    B    2F     normal    Mall    95       800.0      8       100  50.000000
2  811-10003    C    1F  important  Office   177      1200.0      6       250  12.000000
>>> X
   floor_1F  floor_2F  type_Mall  type_Office  type_School  level      area  population  score
0       1.0       0.0        0.0          0.0          1.0    1.0  0.060976    1.000000    1.0
1       0.0       1.0        1.0          0.0          0.0    0.0  0.000000    0.000000    0.5
2       1.0       0.0        0.0          1.0          0.0    1.0  1.000000    0.181818    0.0
>>> y
[0.38596491 1.         0.        ]
```

## Other ways to handle this

{meth}`~pandas.DataFrame.pipe` and {keyword}`def` function ways are ok.

But they are:

- hard to transform to application codes rightly
- hard to debug, and check the processing data
