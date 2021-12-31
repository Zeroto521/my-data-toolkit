# Installation

## Dependencies

Required Dependencies:

- pandas (1.3.4 or later)

Optional Dependencies:

- {mod}`dtoolkit.transformer` requires dependencies

  - scikit-learn (1.0 or later)

- {mod}`dtoolkit.geoaccessor` requires dependencies

  - geopandas (0.9.0 or later)
  - pygeos (0.11.1 or later)

## Install with Conda

To install all DToolKit's dependencies, we recommend to use [the conda package manager](https://conda.io).
The advantage of using the conda package manager is that it provides pre-built binaries for all the required and optional dependencies of DToolKit for all platforms.

Conda will help you get out of many troubles such as the versions of dependencies,
conflicts from channels or environment itself, downloading from where or speed, and so on.

You always can delete a problem conda environment and swift to another good environment.

The following commands create a new environment with the name `dtoolkit_env`,
configures it to install packages always from `conda-forge` channel,
and installs dependencies and DToolKit in it:

### From Command

```bash
conda create -n dtoolkit_env
conda activate dtoolkit_env
conda config --env --add channels conda-forge
conda config --env --set channel_priority strict
conda install python=3 pandas scikit-learn geopandas pygeos
pip install my-data-toolkit
```

### From YAML

Save the following `dtoolkit_env.yaml` YAML to local.

```yaml
name: dtoolkit_env
channels:
  - conda-forge
dependencies:
  - python=3
  - pandas
  - scikit-learn
  - geopandas
  - pygeos
  - pip
  - pip:
      - my-data-toolkit
```

Create the environment from YAML.

```bash
conda env create -f dtoolkit_env.yaml
```

## Install from PyPI

```bash
pip install my-data-toolkit
```

## Install from Source

```bash
pip install git+https://github.com/Zeroto521/my-data-toolkit
```
