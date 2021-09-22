from setuptools import find_packages, setup

NAME = "dtoolkit"
GITHUB_USERNAME = "Zeroto521"
AUTHOR = f"Zero <@{GITHUB_USERNAME}>"

setup(
    name=NAME,
    version=__import__(NAME).__version__,
    author=AUTHOR,
    author_email="Zeroto521@gmail.com",
    url=f"https://github.com/{GITHUB_USERNAME}/my-data-toolkit",
    project_urls={
        "Documentation": "https://my-data-toolkit.readthedocs.io/",
        "Issue Tracker": "https://github.com/zeroto521/my-data-toolkit/issues",
    },
    license=__import__(NAME).__license__,
    description=__import__(NAME).__description__,
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    platforms="any",
    classifiers=[
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
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=["pandas >= 1.1.0"],
)
