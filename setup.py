import os
import sys

from setuptools import setup

# Ensure the current directory is on sys.path so versioneer can be imported
# when pip uses PEP 517/518 build rules.
# https://github.com/python-versioneer/python-versioneer/issues/193
sys.path.append(os.path.dirname(__file__))

from versioneer import get_cmdclass  # noqa: E402

setup(cmdclass=get_cmdclass())
