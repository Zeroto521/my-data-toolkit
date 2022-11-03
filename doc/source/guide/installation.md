# Installation

## Dependencies

### All Python Version Minimal Dependencies

Required Dependencies:

- Python (>= 3.8)
- pandas (>= 1.5.1)

Optional Dependencies:

- {mod}`dtoolkit.transformer` requires dependencies

  - Scikit-learn (>= 1.1)
  - packaging

- {mod}`dtoolkit.geoaccessor` requires dependencies

  - GeoPandas (>= 0.10.0)

### Different Python Version Minimal Dependencies

Dtoolkit support Python version from 3.8 to 3.10.
Therefore each version supports minimal dependencies is different.
You could check the dependencies list from following.

- [Python 3.8 minimal dependencies](https://github.com/Zeroto521/my-data-toolkit/blob/main/ci/env/38-minimal.yaml)
- [Python 3.9 minimal dependencies](https://github.com/Zeroto521/my-data-toolkit/blob/main/ci/env/39-minimal.yaml)
- [Python 3.10 minimal dependencies](https://github.com/Zeroto521/my-data-toolkit/blob/main/ci/env/310-minimal.yaml)
- [Python 3.11 minimal dependencies](https://github.com/Zeroto521/my-data-toolkit/blob/main/ci/env/311-minimal.yaml)

### DToolKit Requires Python Version History

- DToolKit 0.0.1 requires Python 3.7 or 3.8.
- DToolKit 0.0.2 to 0.0.5 require Python 3.7 to 3.9.
- DToolKit 0.0.6 to 0.0.16 require Python 3.7 to 3.10.
- DToolKit 0.0.17 and 0.0.18 require Python 3.8 to 3.10.
- DToolKit 0.0.19 and later require Python 3.8 or newer.

## Install with Mamba

To install all DToolKit's dependencies, we recommend to use [Mamba: The Fast Cross-Platform Package Manager](https://mamba.readthedocs.io/).
The advantage of using the mamba is that it provides pre-built binaries for all the
required and optional dependencies of DToolKit for all platforms and faster to download them.

Mamba will help you get out of many troubles such as the versions of dependencies,
conflicts from channels or environment itself, downloading from where or speed, and so on.

You always can delete that problem environment and swift to another good environment.

The following commands create a new environment with the name `dtoolkit_env`,
then installs dependencies and DToolKit in it:

### From Command

```console
$ mamba create -n dtoolkit_env
$ mamba activate dtoolkit_env
$ mamba install python=3 pandas scikit-learn packaging geopandas
(dtoolkit_env)$ pip install my-data-toolkit
```

### From YAML

Save the following [environment.yaml](../../../environment.yaml) YAML file to local.

```{literalinclude} ../../../environment.yaml
:language: yaml
```

Create the environment from YAML.

```console
$ mamba env create -f environment.yaml
```

## Install from PyPI

```console
$ pip install my-data-toolkit
```

## Install from Source

```{warning}
This's a latest version but not a stable version.
```

```console
$ pip install git+https://github.com/Zeroto521/my-data-toolkit
```
