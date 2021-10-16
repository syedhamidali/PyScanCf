#!/usr/bin/env python
# coding: utf-8

# In[2]:


#!/usr/bin/env python
# coding: utf-8

# ### Author: Syed Hamid Ali - hamidsyed37@gmail.com
# #### Importing Libraries
print('Importing Libraries')
import warnings
warnings.filterwarnings('ignore')
import datetime as dt
tstart = dt.datetime.now()
import numpy as np
import xarray as xr
# import wradlib as wrl
import pandas as pd
from netCDF4 import Dataset
import glob
import os
import pyart
from pyart.config import get_metadata
import warnings
warnings.filterwarnings('ignore')
print('Importing Libraries Done')


# In[3]:


def get_grid(radar):
    """ Returns grid object from radar object. """
    grid = pyart.map.grid_from_radars(
        radar, grid_shape=(40, 500, 500),
        grid_limits=((0, 2e3), (-2e5, 2e5), (-2e5, 2e5)),
        fields=radar.fields.keys(), weighting_function='Barnes2', min_radius=200.)
    return grid

def cfrad(input_dir,output_dir):
    '''
        input_dir = str, Enter path of single sweep data directory
        output_dir = str, Enter the path for output data
    '''
    in_dir=input_dir
    out_dir=output_dir
    files = sorted(glob.glob(in_dir+'//'+'*nc*'))
    print('Number of files: ', len(files))
    bb = list()
    for i in range(0,len(files),10):
        bb.append(files[i:i+10])
    print('Total number of files will be created: ', len(bb))
    print('Merging all scans in one file')
    en=[]; a1=[]; t1=[]; e1=[]; Z1=[]; T1=[]; V1=[]; W1=[]
    for i in range(0,len(bb)):
        en=[]; a1=[]; t1=[]; e1=[]; Z1=[]; T1=[]; V1=[]; W1=[]
        for j in range(0,10):
            ds = Dataset(bb[i][j])
            az = ds.variables['radialAzim'][:]
            time = ds.variables['radialTime'][:]
            ele  = ds.variables['radialElev'][:]
            Z = ds.variables['Z'][:]
            T = ds.variables['T'][:]
            V = ds.variables['V'][:]
            W = ds.variables['W'][:]
            EN = ds.variables['elevationNumber'][:]
            a1.extend(az)
            t1.extend(time)
            e1.extend(ele)
            Z1.extend(Z)
            T1.extend(T)
            V1.extend(V)
            W1.extend(W)
            en.append(EN)
        radar = pyart.testing.make_empty_ppi_radar(996, 3600, 1)
        radar.nsweeps = 10
        radar.time['data'] = np.array(t1)
        radar.time['units'] = ds.variables['radialTime'].units#'seconds since 1970-01-01T00:00:00Z'
        radar.latitude['data'] = np.array([ds.variables['siteLat'][:]])
        radar.longitude['data'] = np.array([ds.variables['siteLon'][:]])
        radar.altitude['data'] = np.array([ds.variables['siteAlt'][:]])
        radar.range['data'] = np.arange(0,ds.dimensions['bin'].size*ds.variables['gateSize'][:].data,
                                        int(ds.variables['gateSize'][:].data))
        radar.fixed_angle['data'] = ds.variables['elevationList']
        radar.sweep_number['data'] = np.array(en)
        radar.sweep_start_ray_index['data'] = np.arange(0,3600,360)
        radar.sweep_end_ray_index['data'] = np.arange(359,3600,360)
        radar.azimuth['data'] = np.ma.array(a1)
        radar.elevation['data'] = np.ma.array(e1)
        radar.metadata['instrument_name'] = 'GOA'
        radar.init_gate_altitude()
        radar.init_gate_longitude_latitude()
        ref_dict = get_metadata('reflectivity')
        ref_dict['data'] = np.ma.array(Z1)
        ref_dict['units'] = 'dBZ'
        radar.fields = {'REF': ref_dict}
        radar.metadata['instrument_name'] = 'GOA'
        VELH_dict = {'units':'m/s','standard_name':'Radial Velocity','data':np.ma.array(V1),}
        radar.add_field('VELH',VELH_dict,replace_existing=True)
        W_dict = {'units':'m/s','standard_name':'Spectral Width','data':np.ma.array(W1),}
        radar.add_field('WIDTHH',W_dict,replace_existing=True)
        T_dict = {'units':'dBT','standard_name':'Total Power','data':np.ma.array(T1),}
        radar.add_field('TP',T_dict,replace_existing=True)
        pyart.io.write_cfradial(out_dir+'/Polar_'+bb[i][0][-24:], radar, 
                                format = 'NETCDF4',time_reference=None, arm_time_variables=False)
        grid = get_grid(radar)
        pyart.io.write_grid(out_dir+'/grid_'+bb[i][0][-24:], grid)
        del radar, grid 
    print('Data merging done \nAll Done \nTotal Time Elapsed: ', dt.datetime.now()-tstart)

