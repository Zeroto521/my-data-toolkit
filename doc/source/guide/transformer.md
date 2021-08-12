# Transformer and Pipeline Quickstart

`Transformer` faces the engineering of **data preprocessing**.

## Applicable Scene

In steps of data preprocessing, we always need to do some **duplication things**.

When we finished dealing with the training dataset, we also need to sort those preprocessing steps out and make them to a function, a API, or something.

## Example

### Sample Data

:::{note}
All data are virtual.
:::

There are some stores sale data of one chain brand.

- These stores place one region.
- Time is one specific year.
- Sale is a year total amount.
- Population is surrounding $200m$ buffer daily people numbers.
- Score is given by the expert, ranges from 0 to 10.

```{code-block} python
>>> import pandas as pd

>>> store_sale_dict = {
...     "code": ["811-10001", "811-10002", "811-10003", "811-10004"],
...     "name": ["A", "B", "C", "D"],
...     "floor": ["1F", "2F", "1F", "B2"],
...     "level": ["strategic", "normal", "impotant", "normal"],
...     "type": ["School", "Mall", "Office", "Home"],
...     "area": [100, 95, 177, 70],
...     "population": [3000, 1000, 2000, 1500],
...     "score": [10, 8, 6, 5],
...     "opendays": [300, 100, 250, 15],
...     "sale": [8000, 5000, 3000, 1500],
... }
>>> df = pd.DataFrame.from_dict(store_sale_dict)
>>> df
        code name floor      level    type  area  population  score  opendays  sale
0  811-10001    A    1F  strategic  School   100        3000     10       300  8000
1  811-10002    B    2F     normal    Mall    95        1000      8       100  5000
2  811-10003    C    1F   impotant  Office   177        2000      6       250  3000
3  811-10004    D    B2     normal    Home    70        1500      5        15  1500
```

### Feature Types and Dealing Steps

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
