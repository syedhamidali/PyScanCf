# PyScanCf

Creates Py-ART compatible cf-radial data from single scans of IMD Radar data

## Description

PyScanCf is a library for creating cfradial (polar) data from IMD radars that contain all 10 sweeps from single scans which are named as (Polar_ABC.nc) as well as gridded radar data from which are named as (grid_ABC.nc). Both formats are compatible for PyART. It uses Pyart to create grid data, so please remember to cite pyart as well.

Installing from source
======================

Installing PyScanCf from source is the only way to get the latest updates and
enhancement to the software that have not yet made it into a release.
The latest source code for PyScanCf can be obtained from the GitHub repository,
https://github.com/syedhamidali/PyScanCf.git.

How to install::

    conda create -n pcf python=3.9 jupyter arm_pyart pandas wradlib -c conda-forge
    conda activate pcf
    pip install git+https://github.com/syedhamidali/PyScanCf.git

Or, to install in your home directory, use::

    git clone https://github.com/syedhamidali/PyScanCf.git
    python setup.py install --user

Or, Install via pip::

    pip install pyscancf
## Please cite this software
Syed H.A, Imran Sayyed, & M.C.R Kalapureddy. (2021). PyScanCf - The library for IMD radar single sweep data. Zenodo. https://doi.org/10.5281/zenodo.5574160
