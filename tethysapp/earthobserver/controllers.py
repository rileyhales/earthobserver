from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tethys_sdk.gizmos import SelectInput, RangeSlider

from .app import Earthobserver as App
from .options import gldas_variables, timecoverage, get_charttypes, gfs_variables, wms_colors, geojson_colors,\
    currentgfs, app_configuration, structure_byvars


@login_required()
def home(request):
    """
    Controller for the home page.
    """
    model = SelectInput(
        display_text='Choose Earth Observation Data',
        name='model',
        multiple=False,
        options=[
            ('(Historical) NASA GLDAS (Global Land Data Assimilation System)', 'gldas'),
            ('(Forecasted) NOAA GFS (Global Forecast System)', 'gfs')
        ],
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
    gldas_options = []
    variables = gldas_variables()
    for key in sorted(variables.keys()):
        tuple1 = (key, variables[key])
        gldas_options.append(tuple1)

    model = SelectInput(
        display_text='Choose Earth Observation Data',
        name='model',
        multiple=False,
        original=True,
        options=[
            ('GLDAS - Global Land Data Assimilation System', 'gldas'),
            ('GFS - Global Forecast System', 'gfs')
        ],
    )

    gldas_vars = SelectInput(
        display_text='Select GLDAS Variable',
        name='gldas_vars',
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

    gfs_vars = SelectInput(
        display_text='Select GFS Variable',
        name='gfs_vars',
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
        display_text='Raster Color Scheme',
        name='colorscheme',
        multiple=False,
        original=True,
        options=wms_colors(),
        initial='rainbow'
    )

    opacity = RangeSlider(
        display_text='Raster Opacity',
        name='opacity',
        min=.5,
        max=1,
        step=.05,
        initial=1,
    )

    gj_color = SelectInput(
        display_text='Boundary - Border Colors',
        name='gjColor',
        multiple=False,
        original=True,
        options=geojson_colors(),
        initial='#ffffff'
    )

    gj_opacity = RangeSlider(
        display_text='Boundary - Border Opacity',
        name='gjOpacity',
        min=0,
        max=1,
        step=.1,
        initial=1,
    )

    gj_weight = RangeSlider(
        display_text='Boundary - Border Thickness',
        name='gjWeight',
        min=1,
        max=5,
        step=1,
        initial=2,
    )

    gj_fillcolor = SelectInput(
        display_text='Boundary - Fill Colors',
        name='gjFillColor',
        multiple=False,
        original=True,
        options=geojson_colors(),
        initial='rgb(0,0,0,0)'
    )

    gj_fillopacity = RangeSlider(
        display_text='Boundary - Fill Opacity',
        name='gjFillOpacity',
        min=0,
        max=1,
        step=.1,
        initial=.5,
    )

    charttype = SelectInput(
        display_text='Choose a Plot Type',
        name='charttype',
        multiple=False,
        original=True,
        options=get_charttypes(),
    )

    context = {
        # data options
        'model': model,
        'gldas_vars': gldas_vars,
        'dates': dates,
        'gfs_vars': gfs_vars,
        'levels': levels,
        'gfsdate': gfsdate,

        # display options
        'colorscheme': colorscheme,
        'opacity': opacity,
        'gjColor': gj_color,
        'gjOpacity': gj_opacity,
        'gjWeight': gj_weight,
        'gjFillColor': gj_fillcolor,
        'gjFillOpacity': gj_fillopacity,
        'charttype': charttype,

        # metadata
        'customsettings': app_configuration(),
        'version': App.version,
    }

    return render(request, 'earthobserver/map.html', context)


@login_required()
def manage(request):
    context = {
        'version': App.version,
    }
    return render(request, 'earthobserver/manage.html', context)
