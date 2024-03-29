import logging
import shutil
import pygrib
import netCDF4
import requests
import numpy
import time as Time
from .options import *


def setenvironment():
    """
    Dependencies: os, shutil, datetime, urllib.request, app_settings (options)
    """
    logging.info('\nSetting the Environment for the GFS Workflow')
    # determine the most day and hour of the day timestamp of the most recent GFS forecast
    now = datetime.datetime.utcnow() - datetime.timedelta(hours=6)
    if now.hour >= 18:
        timestamp = now.strftime("%Y%m%d") + '18'
    elif now.hour >= 12:
        timestamp = now.strftime("%Y%m%d") + '12'
    elif now.hour >= 6:
        timestamp = now.strftime("%Y%m%d") + '06'
    else:   # now.hour >= 0:
        timestamp = now.strftime("%Y%m%d") + '00'
    logging.info('determined the timestamp to download: ' + timestamp)

    # get folder paths for the environment
    threddspath = app_settings()['threddsdatadir']
    threddspath = os.path.join(threddspath, 'gfs')

    # perform a redundancy check, if the last timestamp is the same as current, abort the workflow
    timefile = os.path.join(threddspath, 'last_run.txt')
    try:
        with open(timefile, 'r') as file:
            lasttime = file.readline()
            if lasttime == timestamp:
                # use the redundant check to skip the function because its already been run
                redundant = True
                logging.info('The last recorded timestamp is the timestamp we determined, aborting workflow')
                return threddspath, timestamp, redundant
            elif lasttime == 'clobbered':
                # if you marked clobber is true, dont check for old folders from partially completed workflows
                redundant = False
            else:
                # check to see if there are remnants of partially completed runs and dont destroy old folders
                redundant = False
                test = os.path.join(threddspath, timestamp, 'netcdfs')
                if os.path.exists(test):
                    logging.info('There are directories for this timestep but the workflow wasn\'t finished. '
                                 'Attempting to resume...')
                    return threddspath, timestamp, redundant
    except FileNotFoundError:
        redundant = False

    # create the file structure and their permissions for the new data
    logging.info('Creating THREDDS file structure')
    new_dir = os.path.join(threddspath)
    if os.path.exists(new_dir):
        shutil.rmtree(new_dir)
    os.mkdir(new_dir)
    os.chmod(new_dir, 0o777)
    new_dir = os.path.join(threddspath, timestamp)
    if os.path.exists(new_dir):
        shutil.rmtree(new_dir)
    os.mkdir(new_dir)
    os.chmod(new_dir, 0o777)
    for filetype in ('gribs', 'netcdfs'):
        new_dir = os.path.join(threddspath, timestamp, filetype)
        if os.path.exists(new_dir):
            shutil.rmtree(new_dir)
        os.mkdir(new_dir)
        os.chmod(new_dir, 0o777)

    logging.info('All done setting up folders, on to do work')
    return threddspath, timestamp, redundant


def download_gfs(threddspath, timestamp):
    logging.info('\nStarting GFS grib Downloads')
    # set filepaths
    gribsdir = os.path.join(threddspath, timestamp, 'gribs')

    # This is the List of forecast timesteps for 7 days (6-hr increments)
    fc_steps = ['006', '012', '018', '024', '030', '036', '042', '048', '054', '060', '066', '072', '078', '084']
    # '090', '096', '102', '108', '114', '120', '126', '132', '138', '144', '150', '156', '162', '168']

    # if you already have a folder with data for this timestep, quit this function (you dont need to download it)
    if not os.path.exists(gribsdir):
        logging.info('There is no download folder, you must have already processed them. Skipping download stage.')
        return True
    elif len(os.listdir(gribsdir)) >= len(fc_steps):
        logging.info('There is already gfs data here. Skipping download stage.')
        return True
    # otherwise, remove anything in the folder before starting (in case there was a partial download)
    else:
        shutil.rmtree(gribsdir)
        os.mkdir(gribsdir)
        os.chmod(gribsdir, 0o777)

    # # get the parts of the timestamp to put into the url
    time = datetime.datetime.strptime(timestamp, "%Y%m%d%H").strftime("%H")
    fc_date = datetime.datetime.strptime(timestamp, "%Y%m%d%H").strftime("%Y%m%d")

    for step in fc_steps:
        url = 'https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?file=gfs.t' + time + 'z.pgrb2.0p25.f' + step + \
              '&all_lev=on&all_var=on&dir=%2Fgfs.' + fc_date + '%2F' + time

        file_timestep = datetime.datetime.strptime(timestamp, "%Y%m%d%H")
        file_timestep = file_timestep + datetime.timedelta(hours=int(step))
        file_timestep = file_timestep.strftime("%Y%m%d%H")
        filename = file_timestep + '.grb'

        logging.info('downloading ' + filename + ' (step ' + step + ' of ' + fc_steps[-1] + ')')
        filepath = os.path.join(gribsdir, filename)
        start = Time.time()
        try:
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(filepath, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=10240):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
        except requests.HTTPError as e:
            errorcode = e.response.status_code
            logging.info('\nHTTPError ' + str(errorcode) + ' downloading ' + filename + ' from\n' + url)
            if errorcode == 404:
                logging.info('The file was not found on the server, trying an older forecast time')
            elif errorcode == 500:
                logging.info('Probably a problem with the URL. Check the log and try the link')
            return False
        logging.info('  Download took ' + str(Time.time() - start))
    logging.info('Finished Downloads')
    return True


def set_wmsbounds(threddspath, timestamp):
    logging.info('\nSetting new WMS bounds')
    # setting the environment file paths
    gribs = os.path.join(threddspath, timestamp, 'gribs')
    allgrbs = os.listdir(gribs)
    db = {}

    for grib in allgrbs:
        path = os.path.join(gribs, grib)
        file = pygrib.open(path)
        file.seek(0)
        for data in file:
            minimum = int(data.minimum)
            maximum = int(data.maximum)
            shortname = data.shortName
            if shortname not in db:
                db[shortname] = [minimum, maximum]
            else:
                newmin = min(db[shortname][0], minimum)
                newmax = max(db[shortname][1], maximum)
                db[shortname] = [newmin, newmax]

    formatted = {}
    for var in db:
        bounds = db[var]
        formatted[var] = str(bounds[0]) + ',' + str(bounds[1])

    boundsfile = os.path.join(os.path.dirname(__file__), 'public', 'js', 'bounds.js')
    with open(boundsfile, 'w') as file:
        file.write('const bounds = ' + str(formatted) + ';')
    logging.info('Wrote boundaries to ' + boundsfile)
    return


def grib_to_netcdf(threddspath, timestamp):
    """
    Dependencies: xarray, netcdf4, os, shutil, app_settings (options)
    """
    logging.info('\nStarting Grib Conversions')
    # setting the environment file paths
    gribs = os.path.join(threddspath, timestamp, 'gribs')
    netcdfs = os.path.join(threddspath, timestamp, 'netcdfs')

    # if you already have gfs netcdfs in the netcdfs folder, quit the function
    if not os.path.exists(gribs):
        logging.info('There are no gribs to convert, you must have already run this step. Skipping conversion')
        return
    # otherwise, remove anything in the folder before starting (in case there was a partial conversion)
    else:
        shutil.rmtree(netcdfs)
        os.mkdir(netcdfs)
        os.chmod(netcdfs, 0o777)

    # for each grib file you downloaded, open it, convert it to a netcdf
    files = os.listdir(gribs)
    files = [grib for grib in files if grib.endswith('.grb')]
    for level in gfs_forecastlevels():
        logging.info('working on level ' + level)
        time = 6
        latitudes = [-90 + (i * .25) for i in range(721)]
        longitudes = [-180 + (i * .25) for i in range(1440)]
        time_dt = datetime.datetime.strptime(timestamp, "%Y%m%d%H")
        for file in files:
            # create the new netcdf
            ncname = level + '_' + file.replace('.grb', '.nc')
            ncpath = os.path.join(netcdfs, ncname)
            new_nc = netCDF4.Dataset(ncpath, 'w', clobber=True, format='NETCDF4', diskless=False)

            data_time = time_dt + datetime.timedelta(hours=time)
            data_time = data_time.strftime("%Y%m%d%H")

            new_nc.createDimension('time', 1)
            new_nc.createDimension('lat', 721)
            new_nc.createDimension('lon', 1440)

            new_nc.createVariable(varname='time', datatype='f4', dimensions='time')
            new_nc['time'].axis = 'T'
            new_nc['time'].begin_date = data_time
            new_nc.createVariable(varname='lat', datatype='f4', dimensions='lat')
            new_nc['lat'].axis = 'lat'
            new_nc.createVariable(varname='lon', datatype='f4', dimensions='lon')
            new_nc['lon'].axis = 'lon'

            # set the value of the time variable data
            new_nc['time'][:] = [time]

            # read a file to get the lat/lon variable data
            new_nc['lat'][:] = latitudes
            new_nc['lon'][:] = longitudes

            gribpath = os.path.join(gribs, file)
            gribfile = pygrib.open(gribpath)
            gribfile.seek(0)
            filtered_grib = gribfile(typeOfLevel=level)
            for variable in filtered_grib:
                short = variable.shortName
                if short not in ['time', 'lat', 'lon']:
                    try:
                        new_nc.createVariable(varname=short, datatype='f4', dimensions=('time', 'lat', 'lon'))
                        new_nc[short].units = variable.units
                        new_nc[short].long_name = variable.name
                        new_nc[short].gfs_level = level
                        new_nc[short].begin_date = data_time
                        new_nc[short].axis = 'lat lon'

                        # get array, flip vertical, split and concat to shift from 0-360 degrees to 180-180
                        data = numpy.flip(variable.values, 0)
                        data = numpy.hsplit(data, 2)
                        data = numpy.concatenate((data[1], data[0]), axis=1)
                        new_nc[short][:] = data
                    except:
                        pass
            time += 6
            new_nc.close()
            gribfile.close()

    # delete the gribs now that you're done with them triggering future runs to skip the download step
    shutil.rmtree(gribs)

    logging.info('Conversion Completed')
    return


def new_ncml(threddspath, timestamp):
    logging.info('\nWriting a new ncml file for this date')
    # create a new ncml file by filling in the template with the right dates and writing to a file
    date = datetime.datetime.strptime(timestamp, "%Y%m%d%H")
    date = date.strftime("%Y-%m-%d %H:00:00")
    netcdfs = os.listdir(os.path.join(threddspath, timestamp, 'netcdfs'))
    for level in gfs_forecastlevels():
        ncml = os.path.join(threddspath, level + '_wms.ncml')
        level_ncs = [nc for nc in netcdfs if nc.startswith(level + '_') and nc.endswith('.nc')]
        with open(ncml, 'w') as file:
            file.write(
                '<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n' +
                '   <variable name="time" type="int" shape="time">\n' +
                '      <attribute name="units" value="hours since ' + date + '"/>\n' +
                '      <attribute name="_CoordinateAxisType" value="Time" />\n' +
                '       <values start="0" increment="6" />\n' +
                '   </variable>\n' +
                '   <aggregation dimName="time" type="joinExisting" recheckEvery="5 minutes">\n'
            )
            for nc in level_ncs:
                file.write(
                    '      <netcdf location="' + timestamp + '/netcdfs/' + nc + '"/>\n'
                )
            file.write(
                '   </aggregation>\n' +
                '</netcdf>'
            )
        logging.info('wrote ncml for ' + level)
    return


def cleanup(threddspath, timestamp):
    # delete anything that isn't the new folder of data (named for the timestamp) or the new wms.ncml file
    logging.info('Getting rid of old data folders')
    files = os.listdir(threddspath)
    files.remove(timestamp)
    files = [file for file in files if not file.endswith('.ncml')]
    for file in files:
        try:
            shutil.rmtree(os.path.join(threddspath, file))
        except:
            os.remove(os.path.join(threddspath, file))
    logging.info('Done')
    return


def run_gfs_workflow():
    """
    The controller for running the workflow to download and process data
    """
    # start the workflow by setting the environment
    threddspath, timestamp, redundant = setenvironment()

    # if this has already been done for the most recent forecast, abort the workflow
    if redundant:
        logging.info('\nWorkflow aborted on ' + datetime.datetime.utcnow().strftime("%D at %R"))
        return 'Workflow Aborted- already run for most recent data'

    # run the workflow
    logging.info('\nBeginning to process on ' + datetime.datetime.utcnow().strftime("%D at %R"))

    # get data from the gribs
    succeeded = download_gfs(threddspath, timestamp)
    if not succeeded:
        return 'Workflow Aborted- Downloading Errors Occurred'
    # set_wmsbounds(threddspath, timestamp)

    # convert to netcdfs
    grib_to_netcdf(threddspath, timestamp)
    new_ncml(threddspath, timestamp)

    # finish things up
    cleanup(threddspath, timestamp)
    logging.info('\nAll finished- writing the timestamp used on this run to a txt file')
    with open(os.path.join(threddspath, 'last_run.txt'), 'w') as file:
        file.write(timestamp)

    logging.info('\n\nGFS Workflow completed successfully on ' + datetime.datetime.utcnow().strftime("%D at %R"))
    return 'GFS Workflow Completed- Normal Finish'


if __name__ == '__main__':
    run_gfs_workflow()
