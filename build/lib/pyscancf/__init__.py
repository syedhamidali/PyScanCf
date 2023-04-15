"""
PyScanCf - Python Package to interact with IMD radar data
==================================
Top-level package (:mod:`pyscancf`)
==================================
.. currentmodule:: pyscancf
"""

from pyscancf.pyscancf import cfrad, get_grid
from pyscancf.maxcappi import plot_cappi
import warnings as _warnings
from . import _version_ as _v

_warnings.filterwarnings("always", category=DeprecationWarning, module="pyscancf")

__version__ = _v.get_version()

citation_text = "## Cite PyScanCf:\n\n## Syed, H. A., Sayyed, I., Kalapureddy, M. C. R., & Grandhi, K. K. " \
                "(2021). \n## PyScanCf – The library for single sweep datasets of IMD weather radars. " \
                "\n## Zenodo. doi:10.5281/zenodo.5574160.\n"
print(citation_text)

__all__ = [s for s in dir() if not s.startswith('_')]
