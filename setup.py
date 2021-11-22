from setuptools import setup

from versioneer import get_cmdclass
from versioneer import get_version

setup(
    version=get_version(),
    cmdclass=get_cmdclass(),
)
