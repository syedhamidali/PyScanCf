from io import open
from os import path

from setuptools import find_packages, setup

from pyscancf import _version_ as _v

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pyscancf",
    version=_v._vers,
    author="Hamid Ali Syed",
    description="Creates cf-radial1 data from individual \
        sweeps of IMD DWR data",  # Optional
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  # Optional (see note above)
    url="https://github.com/syedhamidali/PyScanCf",  # Optional
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="IMD Radar cf-radial single sweeps radar weather meteorology",  # Optional
    packages=find_packages(exclude=["contrib", "docs", "tests"]),  # Required
    install_requires=["numpy", "arm_pyart", "netCDF4", "cartopy", "pandas"],  # Required
    project_urls={  # Optional
        "Bug Reports": "https://github.com/syedhamidali/PyScanCf/issues",
        "Source": "https://github.com/syedhamidali/PyScanCf/",
    },
)
