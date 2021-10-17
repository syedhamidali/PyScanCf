# PyScanCf

Creates PyArt compatible cf-radial data from single scans of IMD Radar data

## Description

PyScanCf is a library for creating cfradial (polar) data from IMD radars that contain all 10 sweeps from single scans which are named as (Polar_ABC.nc) as well as gridded radar data from which are named as (grid_ABC.nc). Both formats are compatible for PyART. It uses Pyart to create grid data, so please remember to cite pyart as well.

Installing from source
======================

Installing PyScanCf from source is the only way to get the latest updates and
enhancement to the software that have not yet made it into a release.
The latest source code for PyScanCf can be obtained from the GitHub repository,
https://github.com/syedhamidali/PyScanCf.git. Either download and unpack the 
`zip file <https://github.com/syedhamidali/PyScanCf/archive/refs/heads/master.zip>`_ of 
the source code or use git to checkout the repository::

    pip install git+https://github.com/syedhamidali/PyScanCf.git

Or, to install in your home directory, use::

    git clone https://github.com/syedhamidali/PyScanCf.git
    python setup.py install --user

## Reference
[![DOI](https://zenodo.org/badge/417933645.svg)](https://zenodo.org/badge/latestdoi/417933645)

### Cite as
HA Syed, Imran Sayyed, & MCR Kalapureddy. (2021). PyScanCf - The library for IMD radar single sweep data (1.0.6). Zenodo. https://doi.org/10.5281/zenodo.5574305
