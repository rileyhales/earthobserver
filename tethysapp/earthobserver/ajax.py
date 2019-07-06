import ast
import os

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .options import gldas_variables
from .charts import getchart
from .app import Earthobserver as App


@login_required()
def getChart(request):
    """
    Used to make a timeseries of a variable at a user drawn point
    Dependencies: gldas_variables (options), pointchart (tools), ast, makestatplots (tools)
    """
    data = ast.literal_eval(request.body.decode('utf-8'))
    data['user'] = request.user
    data = getchart(data)
    return JsonResponse(data)


@login_required()
def uploadshapefile(request):
    files = request.FILES.getlist('files')
    user_workspace = App.get_user_workspace(request.user).path

    for n, file in enumerate(files):
        with open(os.path.join(user_workspace, file.name), 'wb') as dst:
            for chunk in files[n].chunks():
                dst.write(chunk)

    return JsonResponse({'status': 'succeeded'})
