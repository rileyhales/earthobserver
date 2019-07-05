import datetime
import os

from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes

from .options import app_configuration, get_gfsdate, get_eodatamodels, gldas_variables, gfs_forecastlevels
from .charts import getchart


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def getcapabilities(request):
    return JsonResponse({
        'api_calls': ['getcapabilities', 'eodatamodels', 'gldasvariables', 'gldasdates', 'gfsdates', 'gfslevels',
                      'timeseries']
    })


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def eodatamodels(request):
    return JsonResponse({'models': get_eodatamodels()})


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def gldasdates(request):
    path = app_configuration()['threddsdatadir']
    path = os.path.join(path, 'gldas', 'raw')
    files = os.listdir(path)
    files.sort()
    start = datetime.datetime.strptime(files[0], "GLDAS_NOAH025_M.A%Y%m.021.nc4").strftime("%B %Y")
    end = datetime.datetime.strptime(files[-1], "GLDAS_NOAH025_M.A%Y%m.021.nc4").strftime("%B %Y")
    dates = {
        'start': start,
        'end': end,
        'api_calls': 'Provide a string type 4 digit year or "alltimes"',
    }
    return JsonResponse(dates)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def gldasvariables(request):
    return JsonResponse(gldas_variables())


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def gfslevels(request):
    return JsonResponse({'levels': gfs_forecastlevels()})


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def gfsdates(request):
    threddspath = app_configuration()['threddsdatadir']
    timestamp = get_gfsdate()
    if not timestamp == 'clobbered':
        gfs_time = datetime.datetime.strptime(timestamp, "%Y%m%d%H")
        gfs_time = gfs_time.strftime("%b %d, %I%p UTC")
    else:
        gfs_time = 'You attempted to overwrite existing data'

    path = os.path.join(threddspath, 'gfs', timestamp, 'netcdfs')
    files = os.listdir(path)
    files = [i for i in files if i.endswith('.nc')]
    files.sort()
    num_files = len(files)
    if num_files != 0:
        gfs_files = num_files

        gfs_start = files[0].split('_')[1]
        gfs_start = gfs_start.replace('.nc', '')
        gfs_start = datetime.datetime.strptime(gfs_start, '%Y%m%d%H')
        gfs_start = gfs_start.strftime("%B %d %Y at %H")

        gfs_end = files[-1].split('_')[1]
        gfs_end = gfs_end.replace('.nc', '')
        gfs_end = datetime.datetime.strptime(gfs_end, '%Y%m%d%H')
        gfs_end = gfs_end.strftime("%B %d %Y at %H")
    else:
        gfs_files = 'No available data'
        gfs_start = 'No available data'
        gfs_end = 'No available data'
    return JsonResponse({
        'gfs_time': gfs_time,
        'gfs_files': gfs_files,
        'gfs_start': gfs_start,
        'gfs_end': gfs_end,
    })


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def timeseries(request):
    parameters = request.GET
    data = {}

    # use try/except to make data dictionary because we want to check that all params have been given
    try:
        data['model'] = parameters['model']
        data['variable'] = parameters['variable']
        data['coords'] = parameters.getlist('coords')
        data['loc_type'] = parameters['loc_type']

        if data['loc_type'] == 'Shapefile':
            data['region'] = parameters['region']

        if data['model'] == 'gldas':
            data['time'] = parameters['time']
        elif data['model'] == 'gfs':
            data['level'] = parameters['level']

    except KeyError as e:
        return JsonResponse({'Missing Parameter': str(e).replace('"', '').replace("'", '')})
    return JsonResponse(getchart(data))
