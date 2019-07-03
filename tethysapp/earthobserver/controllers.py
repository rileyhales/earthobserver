from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tethys_sdk.gizmos import SelectInput, RangeSlider

from .app import Earthobserver as App
from .options import gldas_variables, timecoverage, get_charttypes, gfs_variables, wms_colors, geojson_colors,\
    currentgfs, app_configuration, structure_byvars, get_eodatamodels


@login_required()
def home(request):
    """
    Controller for the home page.
    """
    model = SelectInput(
        display_text='Choose Earth Observation Data',
        name='model',
        multiple=False,
        options=get_eodatamodels(),
        initial=False
    )
    context = {
        'model': model,
        # metadata
        'version': App.version,
    }
    return render(request, 'earthobserver/home.html', context)


@login_required()
def map(request):
    """
    Controller for the map page.
    """
    # get/check information from AJAX request
    post_info = request.GET
    model = post_info.getlist('model')[0]

    if model == 'gldas':
        modelname = 'NASA GLDAS Data'

        gldas_options = []
        variables = gldas_variables()
        for key in sorted(variables.keys()):
            tuple1 = (key, variables[key])
            gldas_options.append(tuple1)

        variables = SelectInput(
            display_text='Select GLDAS Variable',
            name='variables',
            multiple=False,
            original=True,
            options=gldas_options,
        )

        dates = SelectInput(
            display_text='Time Interval',
            name='dates',
            multiple=False,
            original=True,
            options=timecoverage(),
            initial='alltimes'
        )
        charttype = SelectInput(
            display_text='Choose a Plot Type',
            name='charttype',
            multiple=False,
            original=True,
            options=get_charttypes(),
        )

    elif model == 'gfs':
        modelname = 'NOAA GFS Data'

        variables = SelectInput(
            display_text='Select GFS Variable',
            name='variables',
            multiple=False,
            original=True,
            options=gfs_variables(),
        )
        levels = SelectInput(
            display_text='Available Forecast Levels',
            name='levels',
            multiple=False,
            original=True,
            options=structure_byvars()['al'],
        )
        gfsdate = currentgfs()

    colorscheme = SelectInput(
        display_text='EO Data Color Scheme',
        name='colorscheme',
        multiple=False,
        original=True,
        options=wms_colors(),
        initial='rainbow'
    )

    opacity = RangeSlider(
        display_text='EO Data Layer Opacity',
        name='opacity',
        min=.5,
        max=1,
        step=.05,
        initial=1,
    )

    gj_color = SelectInput(
        display_text='Boundary Border Colors',
        name='gjClr',
        multiple=False,
        original=True,
        options=geojson_colors(),
        initial='#ffffff'
    )

    gj_opacity = RangeSlider(
        display_text='Boundary Border Opacity',
        name='gjOp',
        min=0,
        max=1,
        step=.1,
        initial=1,
    )

    gj_weight = RangeSlider(
        display_text='Boundary Border Thickness',
        name='gjWt',
        min=1,
        max=5,
        step=1,
        initial=2,
    )

    gj_fillcolor = SelectInput(
        display_text='Boundary Fill Color',
        name='gjFlClr',
        multiple=False,
        original=True,
        options=geojson_colors(),
        initial='rgb(0,0,0,0)'
    )

    gj_fillopacity = RangeSlider(
        display_text='Boundary Fill Opacity',
        name='gjFlOp',
        min=0,
        max=1,
        step=.1,
        initial=.5,
    )

    context = {
        # data options
        'model': model,
        'modelname': modelname,
        'variables': variables,
        # also model specific options

        # display options
        'colorscheme': colorscheme,
        'opacity': opacity,
        'gjClr': gj_color,
        'gjOp': gj_opacity,
        'gjWt': gj_weight,
        'gjFlClr': gj_fillcolor,
        'gjFlOp': gj_fillopacity,

        # metadata
        'customsettings': app_configuration(),
        'version': App.version,
    }

    if model == 'gldas':
        context['dates'] = dates
        context['charttype'] = charttype
    elif model =='gfs':
        context['levels'] = levels
        context['gfsdate'] = gfsdate

    return render(request, 'earthobserver/map.html', context)


@login_required()
def apihelp(request):
    context = {
        'version': App.version,
    }
    return render(request, 'earthobserver/apihelp.html', context)


@login_required()
def manage(request):
    context = {
        'version': App.version,
    }
    return render(request, 'earthobserver/manage.html', context)
