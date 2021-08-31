from __future__ import print_function

import os

from setuptools import find_packages, setup

NAME = "dtoolkit"
GITHUB_USERNAME = "Zeroto521"
AUTHOR = f"Zero <@{GITHUB_USERNAME}>"
AUTHOR_EMAIL = "Zeroto521@gmail.com"

VERSION = __import__(NAME).__version__
LICENSE = __import__(NAME).__license__
DESCRIPTION = __import__(NAME).__description__
LONG_DESCRIPTION = open("README.md", "r").read()

repository_name = os.path.basename(os.getcwd())
GITHUB_URL = f"https://github.com/{GITHUB_USERNAME}/{repository_name}"

PROJECT_URLS = {
    "Documentation": "https://my-data-toolkit.readthedocs.io/",
    "Issue Tracker": "https://github.com/zeroto521/my-data-toolkit/issues",
}

CLASSIFIERS = [
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Developers",
    "Intended Audience :: Education",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: MacOS",
    "Operating System :: Unix",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Topic :: Scientific/Engineering",
    "Topic :: Scientific/Engineering :: GIS",
    "Topic :: Scientific/Engineering :: Information Analysis",
]

INSTALL_REQUIRES = ["pandas >= 1.1.0"]


setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=GITHUB_URL,
    project_urls=PROJECT_URLS,
    license=LICENSE,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    platforms="any",
    classifiers=CLASSIFIERS,
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=INSTALL_REQUIRES,
)
