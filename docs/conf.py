# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.


# -- Project information -----------------------------------------------------
import datetime
import os
import sys

import pyscancf

project = "PyScanCf"
copyright = "2025, PyScanCf"
author = "Hamid Ali Syed"

# The full version, including alpha/beta/rc tags

sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("../pyscancf"))

# with open("../pyscancf/_version_.py") as f:
#     exec(f.read())
# version = _vers

version = pyscancf.__version__

release = version
html_title = project

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.githubpages",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "IPython.sphinxext.ipython_directive",
    "IPython.sphinxext.ipython_console_highlighting",
    "matplotlib.sphinxext.plot_directive",
    "sphinx.ext.napoleon",
    "sphinx_copybutton",
    "myst_nb",
]

numpydoc_show_class_members = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "pydata_sphinx_theme"

needs_sphinx = "2.1"

# Generate the API documentation when building
autoclass_content = "both"

autosummary_generate = True
autosummary_imported_members = True

# Otherwise, the Return parameter list looks different from the Parameters list
napoleon_use_rtype = False
# Otherwise, the Attributes parameter list looks different from the Parameters list
napoleon_use_ivar = True
napoleon_include_init_with_doc = False
napoleon_use_param = False


# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_suffix = [".rst", ".md", ".ipynb"]

autodoc_mock_imports = ["pyart", "xradar"]
# The master toctree document.
master_doc = "index"


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Don't execute the jupyter notebooks
# nb_execution_mode = "force"
nb_execution_mode = "off"

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "html_admonition",
    "html_image",
    "replacements",
    "substitution",
]

myst_substitutions = {
    "release": release,
    "today": str(datetime.date.today()),
}
