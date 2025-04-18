"""
PyScanCf - Python Package to interact with IMD radar data
==========================================================
Top-level package (:mod:`pyscancf`)
"""

__author__ = "Hamid Ali Syed"
__email__ = "hamidsyed37@gmail.com"

import warnings as _warnings

# Filter deprecation warnings specific to PyScanCf
_warnings.filterwarnings("always", category=DeprecationWarning, module="pyscancf")

# Import primary components
from .cmapmaker import register_colormap, syed_spectral_vals
from .maxcappi import plot_cappi  # noqa
from .pyscancf import cfrad, get_grid  # noqa

# Version
try:
    from .version import version as __version__
except Exception:
    __version__ = "999"

# Define custom colormap
cmap_data = {
    "SyedSpectral": syed_spectral_vals,
}
SyedSpectral = register_colormap(cmap_data)

# Citation
citation_text = (
    "\n## Cite PyScanCf:\n\n"
    "## Syed, H. A., Sayyed, I., Kalapureddy, M. C. R., & Grandhi, K. K. (2021).\n"
    "## PyScanCf – The library for individual sweep datasets of IMD weather radars.\n"
    "## Zenodo. https://doi.org/10.5281/zenodo.5574160\n"
)

print(citation_text)

# Expose public API
__all__ = [s for s in dir() if not s.startswith("_")]
