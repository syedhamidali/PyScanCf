"""
#!/usr/bin/env python
# coding: utf-8
# Author: Syed Hamid Ali - hamidsyed37@gmail.com
"""

import glob
import logging
import os
import re
import warnings
from datetime import datetime

import numpy as np
import pyart  ## noqa
from netCDF4 import Dataset
from pyart.config import get_metadata  ##noqa

from pyscancf.maxcappi import plot_cappi

from .utils import parse_fields

warnings.filterwarnings("ignore", category=DeprecationWarning)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
tstart = datetime.now()


def get_grid(radar, grid_shape=(30, 500, 500), height=15, length=250):
    """
    Transform Cfradial radar data into a three-dimensional grid representation.

    Parameters
    ----------
    radar : pyart.core.Radar
        The radar object containing the Cfradial data to be transformed.

    grid_shape : tuple, optional
        The shape of the grid to be created in terms of the number of bins
        in the z, y, and x dimensions, respectively. Default is (30, 500, 500).

    height : int, optional
        The altitude or height in kilometers to which the grid will extend.
        Default is 15 km.

    length : int, optional
        The maximum range in kilometers for the radar coverage. Default is 250 km.

    Returns
    -------
    grid : pyart.core.Grid
        A three-dimensional grid representation of the radar data.

    """
    grid = pyart.map.grid_from_radars(
        radar,
        grid_shape=grid_shape,
        grid_limits=(
            (radar.altitude["data"][0], height * 1e3),
            (-length * 1e3, length * 1e3),
            (-length * 1e3, length * 1e3),
        ),
        fields=radar.fields.keys(),
        weighting_function="Barnes2",
        min_radius=length,
    )
    return grid


def natural_sort_key(s, _re=re.compile(r"(\d+)")):
    return [int(t) if i & 1 else t.lower() for i, t in enumerate(_re.split(s))]


def cfrad(
    input_dir,
    output_dir,
    scan_type="B",
    dualpol=False,
    gridder=False,
    plot=None,
    nf=None,
):
    """
    Aggregate radar data into CfRadial1 format.

    Parameters
    ----------
    input_dir : str
        The directory path containing single-sweep radar data files.

    output_dir : str
        The directory path where the output data will be saved in CfRadial1 format.

    scan_type : str, optional
        The scan type, either "B" for short-range PPI (Plan Position Indicator)
        or "C" for long-range PPI. Default is "B".

    dualpol : bool, optional
        Specifies whether the radar data contains dual-polarization products
        such as ZDR (Differential Reflectivity) and RHOHV (Correlation Coefficient).
        Set to True if present, otherwise False. Default is False.

    gridder : bool, optional
        Indicates whether data gridding should be performed. Set to True for data
        gridding, otherwise False. Default is False.

    plot : str, optional
        Type of plots to generate for visualization. Options include "REF" for
        reflectivity, "VEL" for velocity, "WIDTH" for spectrum width, or "ALL" for
        all available plots. Default is None, which generates no plots.

    nf : int, optional
        Number of data files to group together during aggregation. Default is None,
        meaning all available files will be aggregated together.
    """
    in_dir = input_dir
    out_dir = output_dir
    files_list = glob.glob(os.path.join(in_dir, "*nc*"))
    files = sorted(files_list, key=natural_sort_key)
    volumes = []
    nf = nf or (10 if scan_type == "B" else 2)  # Default nf value
    # Split the files into groups based on scan type and nf value
    for i in range(0, len(files), nf):
        volumes.append(files[i : i + nf])
    logging.info(f"Packing {len(files)} sweeps into {len(volumes)} volumes")
    for volume in range(len(volumes)):
        sweep_numbers = []
        azimuth_list = []
        times_list = []
        elev_list = []
        nyquist = []
        unambigrange = []
        logging.info(f"Processing volume {volume+1}")
        tmp_data = {}
        for sweep in range(nf):
            # logging.info(f"Sweep {sweep+1}")
            ds = Dataset(volumes[volume][sweep])
            az = ds.variables["radialAzim"][:]
            time = ds.variables["radialTime"][:]
            ele = ds.variables["radialElev"][:]
            EN = ds.variables["elevationNumber"][:]
            azimuth_list.extend(az)
            times_list.extend(time)
            elev_list.extend(ele)
            sweep_numbers.append(EN)
            nyquist.append(ds.variables["nyquist"][:])
            unambigrange.append(ds.variables["unambigRange"][:])
            fields = parse_fields(ds)
            for var_name, var_value in fields.items():
                if var_name not in tmp_data.keys():
                    tmp_data[var_name] = {k: v for k, v in var_value.items()}
                else:
                    tmp_data[var_name]["data"] = np.ma.concatenate(
                        [tmp_data[var_name]["data"], var_value["data"]]
                    )

        fname = os.path.basename(volumes[volume][0]).split(".nc")[0]

        radar = pyart.testing.make_empty_ppi_radar(
            ds.dimensions["bin"].size, ds.dimensions["radial"].size * nf, 1
        )

        radar.nsweeps = int(nf)

        radar.time["data"] = np.array(times_list)
        # 'seconds since 1970-01-01T00:00:00Z'
        radar.time["units"] = ds.variables["radialTime"].units
        radar.latitude["data"] = np.array([ds.variables["siteLat"][:]])
        radar.longitude["data"] = np.array([ds.variables["siteLon"][:]])
        radar.altitude["data"] = np.array([ds.variables["siteAlt"][:]])
        radar.range["data"] = np.arange(
            0,
            ds.dimensions["bin"].size * ds.variables["gateSize"][:].data,
            int(ds.variables["gateSize"][:].data),
        )

        radar.fixed_angle["data"] = ds.variables["elevationList"][:]

        radar.sweep_number["data"] = np.array(sweep_numbers)

        radar.sweep_start_ray_index["data"] = np.arange(
            0, ds.dimensions["radial"].size * nf, ds.dimensions["radial"].size
        )

        radar.sweep_end_ray_index["data"] = np.arange(
            ds.dimensions["radial"].size - 1,
            ds.dimensions["radial"].size * nf,
            ds.dimensions["radial"].size,
        )

        radar.azimuth["data"] = np.ma.array(azimuth_list)
        radar.elevation["data"] = np.ma.array(elev_list)
        radar.metadata["instrument_name"] = fname[:3]
        radar.init_gate_altitude()
        radar.init_gate_longitude_latitude()
        radar.fields = tmp_data

        out_file = f"cfrad_{fname}.nc"
        out_path = os.path.join(out_dir, out_file)
        os.makedirs(out_dir, exist_ok=True)
        pyart.io.write_cfradial(out_path, radar, format="NETCDF4")
        logging.info(f"Saved {os.path.basename(out_path)}")

        if gridder:
            grid = get_grid(radar)
            if plot is not None:
                if plot == "REF":
                    plot_cappi(grid, "REF")
                if plot == "VEL":
                    plot_cappi(grid, "VEL")
                if plot == "WIDTH":
                    plot_cappi(grid, "WIDTH")
                if plot == "ALL":
                    plot_cappi(grid, "REF")
                    plot_cappi(grid, "VEL")
                    plot_cappi(grid, "WIDTH")
            else:
                pass
            out_file = f"grid_{fname}.nc"
            out_path = os.path.join(out_dir, out_file)
            pyart.io.write_grid(out_path, grid)
            logging.info(f"Saved {os.path.basename(out_path)}")
            del radar, grid
        else:
            pass
    logging.info(f"Data merging done \nTime Taken: {datetime.now() - tstart}")
