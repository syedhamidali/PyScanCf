# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pyscancf",  # Required
    version="1.0.21",  # Required
    author='Syed Hamid Ali',
    description="Creates PyArt compatible cf-radial data from single scans of IMD Radar data",  # Optional
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  # Optional (see note above)
    url="https://github.com/syedhamidali/PyScanCf",  # Optional
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="IMD Radar cf-radial single sweeps radar weather meteorology",  # Optional
    packages=find_packages(exclude=["contrib", "docs", "tests"]),  # Required
    install_requires=["numpy","arm_pyart","netCDF4","wradlib","pandas"], # Required
    project_urls={  # Optional
        "Bug Reports": "https://github.com/syedhamidali/PyScanCf/issues",
        "Source": "https://github.com/syedhamidali/PyScanCf/",
    },
)