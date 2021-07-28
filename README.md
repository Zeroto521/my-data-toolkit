# My Data Toolkit: DToolKit

A series of toolkits to decrease the same work
include geographic calculation, data engineering, and so on.

[![Actions Status](https://github.com/Zeroto521/my-data-toolkit/workflows/Tests/badge.svg)](https://github.com/Zeroto521/my-data-toolkit/actions?query=workflow%3ATests) [![Coverage Status](https://codecov.io/gh/Zeroto521/my-data-toolkit/branch/master/graph/badge.svg)](https://codecov.io/gh/Zeroto521/my-data-toolkit)

## Toolkits Sheet

- **Data Engineering**
  - Data Transform Pipeline
    - Scikit-learn Methods: Pandas in and pandas out
      - `FeatureUnion`
      - `make_union`
      - `MinMaxScaler`
      - `OneHotEncoder`
    - Pandas Methods: Make pandas methods to transformer
      - `AssignTF`
      - `AppendTF`
      - `DropTF`
      - `EvalTF`
      - `FillnaTF`
      - `FilterInTF`
      - `FilterTF`
      - `GetTF`
      - `QueryTF`
      - `ReplaceTF`
      - `SelectDtypesTF`: Select dataframe via dtype
    - Numpy Methods: Make numpy methods to transformer
      - `RavelTF`: Multidimensional to one dimension
  - Pandas Object Accessor
    - `pd_obj.cols()`: Columns accessor
    - `pd_obj.dropinf()`: Drop `inf` accessor
    - `df.filterin()`: Extend `df.isin()` to return real data not bool
- **Geographic Calculation**
  - Geographic Buffer Generation
  - Geometry Coordinates
    - Coordinates Container
    - Coordinates Number Container
    - Coordinates Number Counter

## Dependencies

- Python (>= 3.7)
- Pandas (>= 1.1.0)
- GeoPandas (>= 0.9.0)
- Scikit-learn

## User Installation

Only support to build from source, at present.

```bash
pip install git+https://github.com/Zeroto521/my-data-toolkit
```
