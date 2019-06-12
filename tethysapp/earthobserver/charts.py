import calendar
import datetime
import os
import shutil

import rasterio
import rasterstats
import netCDF4
import numpy

from .options import app_configuration


def pointchart(data):
    """
    Description: generates a timeseries for a given point and given variable defined by the user.
    Arguments: A dictionary object from the AJAX-ed JSON object that contains coordinates and the variable name.
    Author: Riley Hales
    Dependencies: netcdf4, numpy, datetime, os, calendar, app_configuration (options)
    Last Updated: Oct 11 2018
    """
    # input parameters
    var = str(data['variable'])
    coords = data['coords']

    # environment settings
    configs = app_configuration()
    path = configs['threddsdatadir']
    path = os.path.join(path, configs['timestamp'], 'processed')

    # return items
    data['values'] = []

    # list the netcdfs to be processed
    allfiles = os.listdir(path)
    files = [nc for nc in allfiles if nc.endswith('.nc')]
    files.sort()

    # get a list of the latitudes and longitudes and the units
    dataset = netCDF4.Dataset(os.path.join(path, str(files[0])), 'r')
    nc_lons = dataset['lon'][:]
    nc_lats = dataset['lat'][:]
    data['units'] = dataset[var].__dict__['units']
    # get the index number of the lat/lon for the point
    adj_lon_ind = (numpy.abs(nc_lons - coords[0])).argmin()
    adj_lat_ind = (numpy.abs(nc_lats - coords[1])).argmin()
    dataset.close()

    # extract values at each timestep
    i = 1
    for nc in files:
        # get the time value for each file
        dataset = netCDF4.Dataset(os.path.join(path, nc), 'r')
        t_value = dataset['time'].__dict__['begin_date']
        t_value = datetime.datetime.strptime(t_value, "%Y%m%d%H")
        t_delta = 6 * i
        i += 1
        t_step = t_value + datetime.timedelta(hours=t_delta)
        t_step = calendar.timegm(t_step.utctimetuple()) * 1000
        # slice the array at the area you want
        val = float(dataset[var][0, adj_lat_ind, adj_lon_ind].data)
        data['values'].append((t_step, val))
        dataset.close()

    return data


def polychart(data):
    """
    Description: generates a timeseries for a given point and given variable defined by the user.
    Arguments: A dictionary object from the AJAX-ed JSON object that contains coordinates and the variable name.
    Author: Riley Hales
    Dependencies: netcdf4, numpy, datetime, os, calendar, app_configuration (options)
    Last Updated: May 14 2019
    """
    # input parameters
    var = str(data['variable'])
    coords = data['coords'][0]  # 5x2 array 1 row/[lat,lon]/corner (1st repeated), clockwise from bottom-left

    # environment settings
    configs = app_configuration()
    path = configs['threddsdatadir']
    path = os.path.join(path, configs['timestamp'], 'processed')

    # return items
    data['values'] = []

    # list the netcdfs to be processed
    allfiles = os.listdir(path)
    files = [nc for nc in allfiles if nc.endswith('.nc')]
    files.sort()

    # get a list of the latitudes and longitudes and the units
    dataset = netCDF4.Dataset(os.path.join(path, str(files[0])), 'r')
    nc_lons = dataset['lon'][:]
    nc_lats = dataset['lat'][:]
    data['units'] = dataset[var].__dict__['units']
    # get a bounding box of the rectangle in terms of the index number of their lat/lons
    minlon = (numpy.abs(nc_lons - coords[1][0])).argmin()
    maxlon = (numpy.abs(nc_lons - coords[3][0])).argmin()
    maxlat = (numpy.abs(nc_lats - coords[1][1])).argmin()
    minlat = (numpy.abs(nc_lats - coords[3][1])).argmin()
    dataset.close()

    # extract values at each timestep
    i = 1
    for nc in files:
        # get the time value for each file
        dataset = netCDF4.Dataset(os.path.join(path, nc), 'r')
        t_value = dataset['time'].__dict__['begin_date']
        t_value = datetime.datetime.strptime(t_value, "%Y%m%d%H")
        t_delta = 6 * i
        i += 1
        t_step = t_value + datetime.timedelta(hours=t_delta)
        t_step = calendar.timegm(t_step.utctimetuple()) * 1000
        # slice the array at the area you want
        array = dataset[var][0, minlat:maxlat, minlon:maxlon].data
        array[array < -9000] = numpy.nan  # If you have fill values, change the comparator to git rid of it
        array = array.flatten()
        array = array[~numpy.isnan(array)]
        data['values'].append((t_step, float(array.mean())))
        dataset.close()

    return data


def shpchart(data):
    """
    Description: This script accepts a netcdf file in a geographic coordinate system, specifically the NASA GLDAS
        netcdfs, and extracts the data from one variable and the lat/lon steps to create a geotiff of that information.
    Dependencies: netCDF4, numpy, rasterio, rasterstats, os, shutil, calendar, datetime, app_configuration (options)
    Params: View README.md
    Returns: Creates a geotiff named 'geotiff.tif' in the directory specified
    Author: Riley Hales, RCH Engineering, March 2019
    """
    # input parameters
    var = str(data['variable'])
    region = data['region']

    # environment settings
    configs = app_configuration()
    path = configs['threddsdatadir']
    path = os.path.join(path, configs['timestamp'], 'processed')
    wrkpath = configs['app_wksp_path']

    # return items
    data['values'] = []

    # list the netcdfs to be processed
    allfiles = os.listdir(path)
    files = [nc for nc in allfiles if nc.endswith('.nc')]
    files.sort()

    # Remove old geotiffs before filling it
    geotiffdir = os.path.join(wrkpath, 'geotiffs')
    if os.path.isdir(geotiffdir):
        shutil.rmtree(geotiffdir)
    os.mkdir(geotiffdir)

    # read netcdf, create geotiff, zonal statistics, format outputs for highcharts plotting
    for i in range(len(files)):
        # open the netcdf and get metadata
        nc_obj = netCDF4.Dataset(os.path.join(path, str(files[i])), 'r')
        lat = nc_obj.variables['lat'][:]
        lon = nc_obj.variables['lon'][:]
        data['units'] = nc_obj[var].__dict__['units']

        # get the variable's data array
        var_data = nc_obj.variables[var][:]  # this is the array of values for the dataset
        array = numpy.asarray(var_data)[0, :, :]  # converting the data type
        array[array < -9000] = numpy.nan  # use the comparator to drop nodata fills
        array = array[::-1]  # vertically flip array so tiff orientation is right (you just have to, try it)

        # create the timesteps for the highcharts plot
        t_value = (nc_obj['time'].__dict__['begin_date'])
        t_step = datetime.datetime.strptime(t_value, "%Y%m%d%H")
        t_delta = 6 * i
        i += 1
        t_step = t_step + datetime.timedelta(hours=t_delta)
        time = calendar.timegm(t_step.utctimetuple()) * 1000

        # file paths and settings
        shppath = os.path.join(wrkpath, 'shapefiles', region, region.replace(' ', '') + '.shp')
        gtiffpath = os.path.join(wrkpath, 'geotiffs', 'geotiff.tif')
        geotransform = rasterio.transform.from_origin(lon.min(), lat.max(), lat[1] - lat[0], lon[1] - lon[0])

        with rasterio.open(gtiffpath, 'w', driver='GTiff', height=len(lat), width=len(lon), count=1, dtype='float32',
                           nodata=numpy.nan, crs='+proj=latlong', transform=geotransform) as newtiff:
            newtiff.write(array, 1)

        stats = rasterstats.zonal_stats(shppath, gtiffpath, stats="mean")
        data['values'].append((time, stats[0]['mean']))

    if os.path.isdir(geotiffdir):
        shutil.rmtree(geotiffdir)

    return data
