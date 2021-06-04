from __future__ import print_function

import os

from setuptools import find_packages, setup

NAME = "dtoolkit"
GITHUB_USERNAME = "Zeroto521"

try:
    # GitHub Short Description
    SHORT_DESCRIPTION = __import__(NAME).__short_description__
except:
    print("'__short_description__' not found in '%s.__init__.py'!" % NAME)
    SHORT_DESCRIPTION = "No short description!"

try:
    LONG_DESCRIPTION = open("README.md", "r").read()
except:
    LONG_DESCRIPTION = "No long description!"

VERSION = __import__(NAME).__version__
AUTHOR = "Zero"
AUTHOR_EMAIL = "Zeroto521@gmail.com"
MAINTAINER = "Zero"
MAINTAINER_EMAIL = "Zeroto521@gmail.com"

repository_name = os.path.basename(os.getcwd())
URL = "https://github.com/{}/{}".format(GITHUB_USERNAME, repository_name)
DOWNLOAD_URL = "https://github.com/{}/{}/archive/master.zip".format(
    GITHUB_USERNAME, repository_name
)

try:
    LICENSE = __import__(NAME).__license__
except:
    print("'__license__' not found in '%s.__init__.py'!" % NAME)
    LICENSE = ""

PLATFORMS = ["Windows", "MacOS", "Unix"]
CLASSIFIERS = [
    "Development Status :: 1 - Planning",
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
    "Programming Language :: Python :: 3.9",
    "Topic :: Scientific/Engineering",
    "Topic :: Scientific/Engineering :: GIS",
    "Topic :: Scientific/Engineering :: Information Analysis",
]

try:
    with open("requirements.txt", "r") as f:
        REQUIRES = [i.strip() for i in f.readlines()]
except:
    print("'requirements.txt' not found!")
    REQUIRES = []

setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    url=URL,
    license=LICENSE,
    description=SHORT_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    platforms=PLATFORMS,
    classifiers=CLASSIFIERS,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    py_modules=[NAME],
    download_url=DOWNLOAD_URL,
    install_requires=REQUIRES,
)
