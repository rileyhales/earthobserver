import ast

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .options import gldas_variables
from .charts import getchart


@login_required()
def getChart(request):
    """
    Used to make a timeseries of a variable at a user drawn point
    Dependencies: gldas_variables (options), pointchart (tools), ast, makestatplots (tools)
    """
    data = ast.literal_eval(request.body.decode('utf-8'))
    data = getchart(data)

    variables = gldas_variables()
    for key in variables:
        if variables[key] == data['variable']:
            name = key
            data['name'] = name
            break
    return JsonResponse(data)
