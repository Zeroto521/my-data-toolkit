# Installation

## Dependencies

Required Dependencies:

- pandas (1.1.3 or later)

Optional Dependencies:

- {mod}`dtoolkit.transformer` requires dependencies

  - scikit-learn (0.24.0 or later)

- {mod}`dtoolkit.geoaccessor` requires dependencies

  - geopandas (0.9.0 or later)
  - pygeos (0.8 or later)

## Install with Conda

To install all DToolKit's dependencies, we recommend to use [the conda package manager](https://conda.io).
The advantage of using the conda package manager is that it provides pre-built binaries
for all the required and optional dependencies of DToolKit for all platforms.

### Create Virtual Environment

Creating a new environment is not strictly necessary,
but given that installing other packages from different channels may cause dependency conflicts,
it can be good practice to install the dtoolkit in a clean environment starting fresh.

The following commands create a new environment with the name `dtoolkit_env`,
configures it to install packages always from conda-forge, and installs dependencies and DToolKit in it:

```bash
conda create -n dtoolkit_env
conda activate dtoolkit_env
conda config --env --add channels conda-forge
conda config --env --set channel_priority strict
conda install python=3 pandas scikit-learn geopandas pygeos
pip install git+https://github.com/Zeroto521/my-data-toolkit
```

## Install from Source

Only support to build from source, at present.

```bash
pip install git+https://github.com/Zeroto521/my-data-toolkit
```
