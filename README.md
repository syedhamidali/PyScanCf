[![Gitter](https://badges.gitter.im/PyScanCf/Issues.svg)](https://gitter.im/PyScanCf/Issues?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

# PyScanCf

Creates Py-ART compatible cf-radial data from individual sweeps of Indian Meteorological Department (IMD) Radar data

## Description

PyScanCf is a library for creating cfradial (polar) data from IMD radars that contain all 10 sweeps from single scans which are named as (Polar_ABC.nc) as well as gridded radar data from which are named as (grid_ABC.nc). Both formats are compatible for PyART. It uses Pyart to create grid data, so please remember to cite **Py-ART** as well.

Latest Documentation
====================

https://syedha.com/PyScanCf/

Latest Examples
====================

https://github.com/syedhamidali/pyscancf_examples

Installing from source
======================

Installing PyScanCf from source is the only way to get the latest updates and
enhancement to the software that have not yet made it into a release.
The latest source code for PyScanCf can be obtained from the GitHub repository,
https://github.com/syedhamidali/PyScanCf.git.

How to install::

    conda create -n pcf python=3.9 jupyter arm_pyart pandas wradlib git -c conda-forge
    conda activate pcf
    pip install git+https://github.com/syedhamidali/PyScanCf.git

Or, to install in your home directory, use::

    git clone https://github.com/syedhamidali/PyScanCf.git
    python setup.py install --user

Or, Install via pip::

    pip install pyscancf

Citation
========

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5881692.svg)](https://doi.org/10.5281/zenodo.5574160)

Syed, H. A., Sayyed, I., Kalapureddy, M. C. R., & Grandhi, K. K. (2021). PyScanCf – The library for single sweep datasets of IMD weather radars. Zenodo.
[doi:10.5281/zenodo.5574160](https://doi.org/10.5281/zenodo.5574160).

### PyScanCf Tutorial on Youtube
<https://youtu.be/OUrdhe5virA>

### Documentation

Import Library::

    import pyscancf as pcf

Mention the data path::

    inp = '/Users/rizvi/Downloads/goa16'

Convert data to cfradial format::

    pcf.cfrad(inp,inp,True,'REF')

And you'll see the beautiful gridded data plot in your notebook,
the figures will be saved in the directory from where you launched the notebook

![image](https://user-images.githubusercontent.com/35923822/179660426-e191bd08-d455-4ccc-96af-ea9cb14cebf5.png)

Detailed and efficient way to use this toolkit
-------
[Detailed Notebook](https://syedha.com/imd/IMD_radar_data_pyscancf.html)
