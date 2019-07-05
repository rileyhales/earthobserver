import datetime
import os

from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes

from .options import app_configuration, get_gfsdate, get_eodatamodels, gldas_variables
from .charts import getchart


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def getcapabilities(request):
    return JsonResponse({'api_calls': ['getcapabilities', 'eodatamodels', 'gldasdates', 'gfsdates', ]})


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
def gfsdate(request):
    return JsonResponse({'gfsdate': get_gfsdate()})


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
