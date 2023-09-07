"""
PyScanCf - Python Package to interact with IMD radar data
==================================
Top-level package (:mod:`pyscancf`)
==================================
.. currentmodule:: pyscancf
"""

import os
import warnings as _warnings

from . import _version_ as _v
from .cmapmaker import register_colormap
from .maxcappi import plot_cappi
from .pyscancf import cfrad, get_grid

_warnings.filterwarnings("always", category=DeprecationWarning, module="pyscancf")

__version__ = _v.get_version()

citation_text = (
    "## Cite PyScanCf:\n\n## Syed, H. A.,"
    + "Sayyed, I., Kalapureddy, M. C. R., & Grandhi, K. K."
    + "(2021). \n## PyScanCf – The library for "
    + "individual sweep datasets of IMD weather radars. "
    + "\n## Zenodo. doi:10.5281/zenodo.5574160.\n"
)
print(citation_text)

# Get the directory where the __init__.py file is located
data_dir = os.path.dirname(__file__)
register_colormap(data_dir)

__all__ = [s for s in dir() if not s.startswith("_")]
