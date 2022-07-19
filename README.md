[![Gitter](https://badges.gitter.im/PyScanCf/Issues.svg)](https://gitter.im/PyScanCf/Issues?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

# PyScanCf

Creates Py-ART compatible cf-radial data from single scans of IMD Radar data

## Description

PyScanCf is a library for creating cfradial (polar) data from IMD radars that contain all 10 sweeps from single scans which are named as (Polar_ABC.nc) as well as gridded radar data from which are named as (grid_ABC.nc). Both formats are compatible for PyART. It uses Pyart to create grid data, so please remember to cite **Py-ART** as well.

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
## Citation

Syed, Hamid Ali, Sayyed, Imran, Kalapureddy, Madhu Chandra R, & Grandhi, Kishore Kumar. (2021). PyScanCf – The library for single sweep datasets of IMD weather radars. Zenodo. 
https://doi.org/10.5281/zenodo.5574160

### PyScanCf Tutorial on Youtube
https://youtu.be/OUrdhe5virA

### Documentation

Import Library::

    from pyscancf import pyscancf as pcf
    
Mention the data path::

    inp = '/Users/rizvi/Downloads/goa16'
    
Convert data to cfradial format::

    pcf.cfrad(inp,inp,True,'REF')
    
And you'll see the beautiful gridded data plot in your notebook, 
the data will be saved in the directory from where you launched the notebook

![image](https://user-images.githubusercontent.com/35923822/179660426-e191bd08-d455-4ccc-96af-ea9cb14cebf5.png)


    
