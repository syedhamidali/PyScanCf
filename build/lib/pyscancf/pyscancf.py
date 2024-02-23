"""
#!/usr/bin/env python
# coding: utf-8
# Author: Syed Hamid Ali - hamidsyed37@gmail.com
"""

import datetime as dt
import glob
import os
import pathlib
import re
import warnings

import numpy as np
import pyart
from netCDF4 import Dataset
from pyart.config import get_metadata

from pyscancf.maxcappi import plot_cappi

warnings.filterwarnings("ignore")
tstart = dt.datetime.now()


def get_grid(radar, grid_shape=(30, 500, 500), height=15, length=250):
    """
    Returns grid object from radar object.

    grid_shape=(60, 500, 500), no. of bins of z,y,x respectively.

    height:(int) = 15, height in km

    length:(int) = 250, Range of radar in km

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
    Aggregates data to cfradial1 data.
    input_dir(str): Enter path of single sweep data directory,
    output_dir(str): Enter the path for output data,
    scan_type(str): "B", "C". B is for short range PPI,
                & C is for long range PPI.
    dualpol(bool): True, False. (If the data contains
                dual-pol products e.g., ZDR, RHOHV),
    gridder(bool): True, False,
    plot(str): 'REF', 'VEL', 'WIDTH', 'ALL',
    nf(int): Number of files to group together
    """
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)
    in_dir = input_dir
    out_dir = output_dir
    files_list = glob.glob(os.path.join(in_dir, "*nc*"))
    files = sorted(files_list, key=natural_sort_key)
    print("Number of files: ", len(files))
    bb = list()
    if scan_type == "B":
        if nf is None:
            nf = 10
        for i in range(0, len(files), nf):
            bb.append(files[i : i + nf])
    elif scan_type == "C":
        if nf is None:
            nf = 2
        for i in range(0, len(files), nf):
            bb.append(files[i : i + nf])
    print(f"Total no. of output files: {len(bb)}.")
    print("Merging all scans into one Volume")
    for i in range(0, len(bb)):
        en = []
        a1 = []
        t1 = []
        e1 = []
        Z1 = []
        T1 = []
        V1 = []
        W1 = []
        ZDR1 = []
        KDP1 = []
        PHIDP1 = []
        SQI1 = []
        RHOHV1 = []
        HCLASS1 = []
        nyquist = []
        unambigrange = []
        for j in range(0, nf):
            ds = Dataset(bb[i][j])
            az = ds.variables["radialAzim"][:]
            time = ds.variables["radialTime"][:]
            ele = ds.variables["radialElev"][:]
            Z = ds.variables["Z"][:]
            # T = ds.variables['T'][:]
            V = ds.variables["V"][:]
            W = ds.variables["W"][:]
            EN = ds.variables["elevationNumber"][:]
            a1.extend(az)
            t1.extend(time)
            e1.extend(ele)
            Z1.extend(Z)
            # T1.extend(T)
            V1.extend(V)
            W1.extend(W)
            en.append(EN)
            nyquist.append(ds.variables["nyquist"][:])
            unambigrange.append(ds.variables["unambigRange"][:])
            if dualpol:
                if "ZDR" in ds.variables:
                    ZDR = ds.variables["ZDR"][:]
                    ZDR1.extend(ZDR)

                if "PHIDP" in ds.variables:
                    PHIDP = ds.variables["PHIDP"][:]
                    PHIDP1.extend(PHIDP)

                if "KDP" in ds.variables:
                    KDP = ds.variables["KDP"][:]
                    KDP1.extend(KDP)

                if "SQI" in ds.variables:
                    SQI = ds.variables["SQI"][:]
                    SQI1.extend(SQI)

                if "RHOHV" in ds.variables:
                    RHOHV = ds.variables["RHOHV"][:]
                    RHOHV1.extend(RHOHV)

                if "HCLASS" in ds.variables:
                    HCLASS = ds.variables["HCLASS"][:]
                    HCLASS1.extend(HCLASS)


        fname = os.path.basename(bb[i][0]).split(".nc")[0]

        radar = pyart.testing.make_empty_ppi_radar(
            ds.dimensions["bin"].size, ds.dimensions["radial"].size * nf, 1
        )
        radar.nsweeps = nf
        radar.time["data"] = np.array(t1)
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

        radar.fixed_angle["data"] = ds.variables["elevationList"]

        radar.sweep_number["data"] = np.array(en)

        radar.sweep_start_ray_index["data"] = np.arange(
            0, ds.dimensions["radial"].size * nf, ds.dimensions["radial"].size
        )

        radar.sweep_end_ray_index["data"] = np.arange(
            ds.dimensions["radial"].size - 1,
            ds.dimensions["radial"].size * nf,
            ds.dimensions["radial"].size,
        )

        radar.azimuth["data"] = np.ma.array(a1)
        radar.elevation["data"] = np.ma.array(e1)
        radar.metadata["instrument_name"] = fname[:3]
        radar.init_gate_altitude()
        radar.init_gate_longitude_latitude()
        ref_dict = get_metadata("reflectivity")
        ref_dict["data"] = np.ma.array(Z1)
        ref_dict["units"] = "dBZ"
        VEL_dict = get_metadata("velocity")
        VEL_dict["data"] = np.ma.array(V1)
        VEL_dict["units"] = "m/s"
        W_dict = get_metadata("spectrum_width")
        W_dict["data"] = np.ma.array(W1)
        W_dict["units"] = "m/s"
        radar.instrument_parameters = {}
        radar.instrument_parameters["nyquist_velocity"] = {
            "units": "m/s",
            "comments": "Unambiguous velocity",
            "meta_group": "instrument_parameters",
            "long_name": "Nyquist velocity",
        }
        radar.instrument_parameters["nyquist_velocity"]["data"] = np.ma.array(nyquist)
        radar.instrument_parameters["unambiguous_range"] = {
            "units": "meters",
            "comments": "Unambiguous range",
            "meta_group": "instrument_parameters",
            "long_name": "Unambiguous range",
        }
        radar.instrument_parameters["unambiguous_range"]["data"] = np.ma.array(
            unambigrange
        )

        radar.fields = {"REF": ref_dict, "VEL": VEL_dict, "WIDTH": W_dict}

        if dualpol:
            ZDR_dict = get_metadata("differential_reflectivity")
            ZDR_dict["units"] = "dB"
            if "ZDR" in ds.variables:
                ZDR_dict["data"] = np.ma.array(ZDR1)
                radar.fields["ZDR"] = ZDR_dict
            
            PHIDP_dict = get_metadata("differential_phase")
            PHIDP_dict["units"] = "degrees"
            if "PHIDP" in ds.variables:
                PHIDP_dict["data"] = np.ma.array(PHIDP1)
                radar.fields["PHIDP"] = PHIDP_dict
            

            KDP_dict = get_metadata("specific_differential_phase")
            KDP_dict["units"] = "degrees/km"
            if "KDP" in ds.variables:
                KDP_dict["data"] = np.ma.array(KDP1)
                radar.fields["KDP"] = KDP_dict


            RHOHV_dict = get_metadata("cross_correlation_ratio")
            RHOHV_dict["units"] = "unitless"
            if "RHOHV" in ds.variables:
                RHOHV_dict["data"] = np.ma.array(RHOHV1)
                radar.fields["RHOHV"] = RHOHV_dict 
            

            SQI_dict = get_metadata("normalized_coherent_power")
            SQI_dict["units"] = "unitless"
            if "SQI" in ds.variables:
                SQI_dict["data"] = np.ma.array(SQI1)
                radar.fields["SQI"] = SQI_dict
            

            HCLASS_dict = get_metadata("radar_echo_classification")
            HCLASS_dict["units"] = "unitless"
            if "HCLASS" in ds.variables:
                HCLASS_dict["data"] = np.ma.array(HCLASS1)
                radar.fields["HCLASS"] = HCLASS_dict

        out_file = f"cfrad_{fname}.nc"
        out_path = os.path.join(out_dir, out_file)
        pyart.io.write_cfradial(out_path, radar, format="NETCDF4")

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
            del radar, grid
        else:
            pass
    print("Data merging done \nTotal Time Elapsed: ", dt.datetime.now() - tstart)
