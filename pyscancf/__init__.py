"""
PyScanCf - Python Package to interact with IMD radar data
==================================
Top-level package (:mod:`pyscancf`)
==================================
.. currentmodule:: pyscancf
"""

import os
import warnings as _warnings
from .cmapmaker import syed_spectral_vals
from .cmapmaker import register_colormap
from . import _version_ as _v
from .maxcappi import plot_cappi
from .pyscancf import cfrad, get_grid

_warnings.filterwarnings("always", category=DeprecationWarning, module="pyscancf")

__version__ = _v.get_version()

citation_text = (
    "\n## Cite PyScanCf:\n\n## Syed, H. A.,"
    + "Sayyed, I., Kalapureddy, M. C. R., & Grandhi, K. K."
    + "(2021). \n## PyScanCf – The library for "
    + "individual sweep datasets of IMD weather radars. "
    + "\n## Zenodo. doi:10.5281/zenodo.5574160.\n"
)
print(citation_text)

cmap_data = {
    "SyedSpectral": syed_spectral_vals,  # Use the data defined in your script
}

SyedSpectral = register_colormap(cmap_data)
SyedSpectral

__all__ = [s for s in dir() if not s.startswith("_")]
