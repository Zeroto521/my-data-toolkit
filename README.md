# My Data Toolkit: DToolKit

A series of toolkits to decrease the same work
include geographic calculation, data engineering, and so on.

[![Actions Status](https://github.com/Zeroto521/my-data-toolkit/workflows/Tests/badge.svg)](https://github.com/Zeroto521/my-data-toolkit/actions?query=workflow%3ATests) [![Coverage Status](https://codecov.io/gh/Zeroto521/my-data-toolkit/branch/master/graph/badge.svg)](https://codecov.io/gh/Zeroto521/my-data-toolkit)

## Toolkits Sheet

- **Data Engineering**
  - Data Transform Pipeline
    - `GetTF`: `DataFrame` Selector Transformer
    - `RavelTF`: Multidimensional to One Dimension Transformer
    - `QueryTF`: `DataFrame`'s `query` Function Transformer
    - `EvalTF`: `DataFrame`'s `eval` Function Transformer
  - Pandas Object Accessor
    - `pd_obj.cols()`: Pandas Object Columns accessor
    - `pd_obj.dropinf()`: Pandas Object Drop `inf` accessor
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
