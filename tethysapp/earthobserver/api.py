import datetime
import os

from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes

from .options import app_configuration, get_gfsdate, get_eodatamodels, gldas_variables


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
        'api_calls': 'Provide a 4 digit year or "alltimes"',
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
