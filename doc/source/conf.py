# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options.
# For a full list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


# -- Project information -----------------------------------------------------

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
from __future__ import annotations

import inspect
import os
import sys
from datetime import datetime

import dtoolkit

# fmt: off
version = release = (
    dtoolkit.__version__
    .replace(".dev0", "")
    .replace(".post0", "")
)
# fmt: on

project = "My Data Toolkit"
author = "@Zeroto521"
copyright = f"2021-{datetime.now().year} {author}"  # pylint: disable=redefined-builtin
github_url = "https://github.com/Zeroto521/my-data-toolkit"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "myst_parser",
    "numpydoc",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.linkcode",
    "sphinx_toggleprompt",
    "matplotlib.sphinxext.plot_directive",
    "IPython.sphinxext.ipython_console_highlighting",
    "IPython.sphinxext.ipython_directive",
    "nbsphinx",
]

# The suffix of source filenames.
source_suffix = [".rst", ".md"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_template"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "pydata_sphinx_theme"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    "search_bar_position": "sidebar",
    "github_url": github_url,
    "icon_links": [
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/my-data-toolkit",
            "icon": "fas fa-box",
        },
    ],
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


# Add redirect for previously existing pages, each item is like `(from_old, to_new)`

moved_pages = [
    ("py-modindex", "reference"),
]

html_additional_pages = {page[0]: "redirect.html" for page in moved_pages}

html_context = {"redirects": dict(moved_pages)}


nbsphinx_prolog = r"""
{% set docname = env.doc2path(env.docname, base=None) %}

.. tip::

    This page was generated from `{{ docname }}`__.

    __ https://github.com/zeroto521/my-data-toolkit/blob/main/doc/source/{{ docname }}
"""


#  --Options for sphinx extensions -----------------------------------------------

# connect docs in other projects
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "sklearn": ("https://scikit-learn.org/stable/", None),
    "geopandas": ("https://geopandas.org/en/stable/", None),
    "shapely": ("https://shapely.readthedocs.io/en/stable/", None),
    "pyproj": ("https://pyproj4.github.io/pyproj/stable/", None),
    "pygeos": ("https://pygeos.readthedocs.io/en/stable/", None),
    "joblib": ("https://joblib.readthedocs.io/en/latest/", None),
}

# extlinks alias
extlinks = {
    "issue": (f"{github_url}/issues/%s", "issue#%s"),
    "pr": (f"{github_url}/issues/%s", "pr#%s"),
    "user": (r"https://github.com/%s", "@%s"),
}

myst_enable_extensions = [
    "colon_fence",
]

autosummary_generate = True

nbsphinx_execute = "always"
nbsphinx_allow_errors = True


# based on pandas/doc/source/conf.py
def linkcode_resolve(domain: str, info: dict[str, str]) -> str | None:
    """
    Determine the URL corresponding to Python object
    """

    if domain != "py":
        return None

    modname = info["module"]
    fullname = info["fullname"]

    submod = sys.modules.get(modname)
    if submod is None:
        return None

    obj = submod
    for part in fullname.split("."):
        try:
            obj = getattr(obj, part)
        except AttributeError:
            return None

    try:
        fn = inspect.getsourcefile(inspect.unwrap(obj))
    except TypeError:
        fn = None

    if not fn:
        return None

    # to fix these doc doesn't exist in dtoolkit
    if "dtoolkit" not in fn:
        return None

    try:
        source, lineno = inspect.getsourcelines(obj)
    except OSError:
        lineno = None

    linespec = f"#L{lineno}-L{lineno + len(source) - 1}" if lineno else ""
    fn = os.path.relpath(fn, start=os.path.dirname(dtoolkit.__file__))

    base_link = f"{github_url}/blob/" + "{branch}" + f"/dtoolkit/{fn}{linespec}"
    if "post" in version:
        return base_link.format(branch="main")

    return base_link.format(branch=f"v{version}")
