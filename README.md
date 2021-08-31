# My Data Toolkit: DToolKit

[![Actions Status](https://github.com/Zeroto521/my-data-toolkit/workflows/Tests/badge.svg)](https://github.com/Zeroto521/my-data-toolkit/actions?query=workflow%3ATests) [![Coverage Status](https://codecov.io/gh/Zeroto521/my-data-toolkit/branch/master/graph/badge.svg)](https://codecov.io/gh/Zeroto521/my-data-toolkit) [![Documentation Status](https://readthedocs.org/projects/my-data-toolkit/badge/?version=latest)](https://my-data-toolkit.readthedocs.io/en/latest/?badge=latest)

A series of toolkits to decrease the same work
include geographic calculation, data engineering, and so on.

See [documentation](https://my-data-toolkit.readthedocs.io/) for more information.

## Introduction

DToolKit mainly includes following packages:

- [accessor](https://my-data-toolkit.readthedocs.io/en/latest/reference/accessor.html): hook some useful functions into pandas object, use functions like pandas native way.
- [transformer](https://my-data-toolkit.readthedocs.io/en/latest/guide/transformer.html): faces the engineering of data preprocessing.
- [geography](https://my-data-toolkit.readthedocs.io/en/latest/reference/geography.html): some useful geographic functions

## Dependencies

See the [installation docs](https://my-data-toolkit.readthedocs.io/en/latest/guide/installation.html) for all details.
DToolKit depends on the following packages:

- Base
  - Python (>= 3.7)
  - Pandas (>= 1.1.0)
  - packaging
- Optionals
  - GeoPandas (>= 0.9.0)
  - Scikit-learn (>= 0.24.0)
  - More-Itertools (>=7.1.0)

## Note

DToolKit is under heavy development.
While the available functionality should be stable and working correctly,
it's still possible that APIs change in upcoming releases.
