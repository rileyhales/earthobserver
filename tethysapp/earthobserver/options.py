from .app import Earthobserver as App
import os
import datetime


def app_configuration():
    """
    Gets the settings for the app for use in other functions and ajax for leaflet
    Dependencies: os, App (app)
    """
    return {
        'app_wksp_path': os.path.join(App.get_app_workspace().path, ''),
        'threddsdatadir': App.get_custom_setting("Local Thredds Folder Path"),
        'threddsurl': App.get_custom_setting("Thredds WMS URL"),
        'geoserverurl': App.get_custom_setting("Geoserver Workspace URL"),
        'timestamp': get_gfsdate(),
        'logfile': os.path.join(App.get_app_workspace().path, 'workflow.log')
    }


def get_eodatamodels():
    return [
            ('(Historical) NASA GLDAS (Global Land Data Assimilation System)', 'gldas'),
            ('(Forecasted) NOAA GFS (Global Forecast System)', 'gfs')
        ]


def get_gfsdate():
    with open(os.path.join(App.get_app_workspace().path, 'gfstimestamp.txt'), 'r') as file:
        return file.read()


def currentgfs():
    # if there is actually data in the app, then read the file with the timestamp on it
    path = App.get_custom_setting("Local Thredds Folder Path")
    timestamp = get_gfsdate()
    path = os.path.join(path, 'gfs', timestamp)
    if os.path.exists(path):
        timestamp = datetime.datetime.strptime(timestamp, "%Y%m%d%H")
        return "This GFS data from " + datetime.datetime.strftime(timestamp, "%b %d, %I%p UTC")
    return "No GFS data detected"


def gfs_variables():
    return [
        ('Albedo', 'al'), ('Apparent temperature', 'aptmp'), ('Absolute vorticity', 'absv'),
        ('Best (4-layer) lifted index', '4lftx'), ('Total Cloud Cover', 'tcc'), ('Cloud mixing ratio', 'clwmr'),
        ('Convective available potential energy', 'cape'), ('Convective inhibition', 'cin'),
        ('Categorical ice pellets', 'cicep'), ('Categorical freezing rain', 'cfrzr'), ('Categorical rain', 'crain'),
        ('Convective precipitation (water)', 'acpcp'), ('Categorical snow', 'csnow'),
        ('Convective precipitation rate', 'cprat'), ('Cloud water', 'cwat'), ('Cloud work function', 'cwork'),
        ('Downward short-wave radiation flux', 'dswrf'), ('Downward long-wave radiation flux', 'dlwrf'),
        ('Field Capacity', 'fldcp'), ('Geopotential Height', 'gh'), ('Graupel (snow pellets)', 'grle'),
        ('Geometric vertical velocity', 'wz'), ('Ground heat flux', 'gflux'), ('Haines Index', 'hindex'),
        ('Ice water mixing ratio', 'icmr'), ('ICAO Standard Atmosphere reference height', 'icaht'),
        ('Icing severity', 'ICSEV'), ('Latent heat net flux', 'lhtfl'), ('Land-sea mask', 'lsm'),
        ('Maximum/Composite radar reflectivity', 'refc'), ('Maximum temperature', 'tmax'),
        ('Minimum temperature', 'tmin'), ('Momentum flux, u component', 'uflx'), ('Momentum flux, v component', 'vflx'),
        ('Meridional flux of gravity wave stress', 'v-gwd'), ('MSLP (Eta model reduction)', 'mslet'),
        ('Orography', 'orog'), ('Ozone mixing ratio', 'o3mr'), ('Total ozone', 'tozne'), ('Pressure', 'pres'),
        ('Pressure of level from which parcel was lifted', 'plpl'), ('Potential temperature', 'pt'),
        ('Potential evaporation rate', 'pevpr'), ('Precipitation rate', 'prate'),
        ('Percent frozen precipitation', 'cpofp'), ('Pressure reduced to MSL', 'prmsl'), ('Precipitable water', 'pwat'),
        ('Planetary boundary layer height', 'hpbl'), ('Rain mixing ratio', 'rwmr'), ('Relative humidity', 'r'),
        ('Soil Temperature', 'st'), ('Specific humidity', 'q'), ('Surface pressure', 'sp'), ('Snow depth', 'sde'),
        ('Sunshine Duration', 'SUNSD'), ('Sensible heat net flux', 'shtfl'), ('Surface lifted index', 'lftx'),
        ('Sea ice area fraction', 'ci'), ('Snow mixing ratio', 'snmr'), ('Storm relative helicity', 'hlcy'),
        ('Temperature', 't'), ('Total Precipitation', 'tp'), ('U-component storm motion', 'ustm'),
        ('U component of wind', 'u'), ('Upward short-wave radiation flux', 'uswrf'),
        ('Upward long-wave radiation flux', 'ulwrf'), ('V-component storm motion', 'vstm'),
        ('Volumetric soil moisture content', 'soilw'), ('V component of wind', 'v'), ('Vertical velocity', 'w'),
        ('Vertical speed shear', 'vwsh'), ('Ventilation Rate', 'VRATE'), ('Visibility', 'vis'),
        ('Wind speed (gust)', 'gust'), ('Water equivalent of accumulated snow depth', 'sdwe'), ('Water runoff', 'watr'),
        ('Wilting Point', 'wilt'), ('Zonal flux of gravity wave stress', 'u-gwd'),
        ('2 metre temperature', '2t'), ('2 metre dewpoint temperature', '2d'), ('2 metre relative humidity', '2r'),
        ('5-wave geopotential height', '5wavh'), ('10 metre U wind component', '10u'),
        ('10 metre V wind component', '10v'), ('100 metre U wind component', '100u'),
        ('100 metre V wind component', '100v'),
    ]


def gldas_variables():
    """
    List of the plottable variables from the GLDAS 2.1 datasets used
    """
    return {
        'Air Temperature': 'Tair_f_inst',
        'Surface Albedo': 'Albedo_inst',
        'Surface Temperature': 'AvgSurfT_inst',
        'Canopy Water Amount': 'CanopInt_inst',
        'Evaporation Flux From Canopy': 'ECanop_tavg',
        'Evaporation Flux From Soil': 'ESoil_tavg',
        'Water Evaporation Flux': 'Evap_tavg',
        'Surface Downwelling Longwave Flux In Air': 'LWdown_f_tavg',
        'Surface Net Downward Longwave Flux': 'Lwnet_tavg',
        'Potential Evaporation Flux': 'PotEvap_tavg',
        'Surface Air Pressure': 'Psurf_f_inst',
        'Specific Humidity': 'Qair_f_inst',
        'Downward Heat Flux In Soil': 'Qg_tavg',
        'Surface Upward Sensible Heat Flux': 'Qh_tavg',
        'Surface Upward Latent Heat Flux': 'Qle_tavg',
        'Surface Runoff Amount': 'Qs_acc',
        'Subsurface Runoff Amount': 'Qsb_acc',
        'Surface Snow Melt Amount': 'Qsm_acc',
        'Precipitation Flux': 'Rainf_f_tavg',
        'Rainfall Flux': 'Rainf_tavg',
        'Root Zone Soil Moisture': 'RootMoist_inst',
        'Surface Snow Amount': 'SWE_inst',
        'Soil Temperature': 'SoilTMP0_10cm_inst',
        'Surface Downwelling Shortwave Flux In Air': 'SWdown_f_tavg',
        'Surface Snow Thickness': 'SnowDepth_inst',
        'Snowfall Flux': 'Snowf_tavg',
        'Surface Net Downward Shortwave Flux': 'Swnet_tavg',
        'Transpiration Flux From Veg': 'Tveg_tavg',
        'Wind Speed': 'Wind_f_inst',
        }


def timecoverage():
    """
    Time intervals of GLDAS data
    """
    return [
        ('All Available Times', 'alltimes'),
        (2019, 2019),
        (2018, 2018),
        (2017, 2017),
        (2016, 2016),
        (2015, 2015),
        (2014, 2014),
        (2013, 2013),
        (2012, 2012),
        (2011, 2011),
        (2010, 2010),
        (2009, 2009),
        (2008, 2008),
        (2007, 2007),
        (2006, 2006),
        (2005, 2005),
        (2004, 2004),
        (2003, 2003),
        (2002, 2002),
        (2001, 2001),
        (2000, 2000),
    ]


def wms_colors():
    """
    Color options usable by thredds wms
    """
    return [
        ('SST-36', 'sst_36'),
        ('Greyscale', 'greyscale'),
        ('Rainbow', 'rainbow'),
        ('OCCAM', 'occam'),
        ('OCCAM Pastel', 'occam_pastel-30'),
        ('Red-Blue', 'redblue'),
        ('NetCDF Viewer', 'ncview'),
        ('ALG', 'alg'),
        ('ALG 2', 'alg2'),
        ('Ferret', 'ferret'),
        ]


def geojson_colors():
    return [
        ('White', '#ffffff'),
        ('Transparent', 'rgb(0,0,0,0)'),
        ('Red', '#ff0000'),
        ('Green', '#00ff00'),
        ('Blue', '#0000ff'),
        ('Black', '#000000'),
        ('Pink', '#ff69b4'),
        ('Orange', '#ffa500'),
        ('Teal', '#008080'),
        ('Purple', '#800080'),
    ]


def get_charttypes():
    return [
        ('Full Timeseries (Single-Line Plot)', 'timeseries'),
        ('Monthly Analysis (Box Plot)', 'monthbox'),
        ('Monthly Analysis (Multi-Line Plot)', 'monthmulti'),
        ('Yearly Analysis (Box Plot)', 'yearbox'),
        ('Yearly Analysis (Multi-Line Plot)', 'yearmulti'),
    ]


def gfs_forecastlevels():
    tuples = [
        ('Atmosphere', 'atmosphere'),
        ('At A Depth Below Land Layer', 'depthBelowLandLayer'),
        ('At A Height Above Ground', 'heightAboveGround'),  # nope
        ('At A Height Above Ground Layer', 'heightAboveGroundLayer'),
        ('At A Height Above the Sea', 'heightAboveSea'),
        ('Hybrid Level', 'hybrid'),
        ('Isothermal (0 Celcius)', 'isothermZero'),
        ('Isobaric (Pa)', 'isobaricInPa'),  # nope
        ('Isobaric (hPa)', 'isobaricInhPa'),  # nope
        ('Max Wind', 'maxWind'),
        ('Mean Sea Level', 'meanSea'),
        ('Nominal Top', 'nominalTop'),
        ('Potential Vorticity', 'potentialVorticity'),
        ('Pressure From Ground Layer', 'pressureFromGroundLayer'),
        ('Sigma', 'sigma'),
        ('Sigma Layer', 'sigmaLayer'),
        ('Surface', 'surface'),
        ('Tropopause', 'tropopause'),
        ('Unknown', 'unknown')
    ]
    return [
        'atmosphere',
        'depthBelowLandLayer',
        'heightAboveGround',  # nope
        'heightAboveGroundLayer',
        'heightAboveSea',
        'hybrid',
        'isothermZero',
        'isobaricInPa',
        'isobaricInhPa',  # nope
        'maxWind',
        'meanSea',
        'nominalTop',
        'potentialVorticity',
        'pressureFromGroundLayer',  # nope
        'sigma',
        'sigmaLayer',
        'surface',  # nope
        'tropopause',
        'unknown',  # nope
    ]


def structure_byvars():
    return {
        'refc': [('Atmosphere', 'atmosphere')],
        'tcc': [('Atmosphere', 'atmosphere'), ('Isobaric (hPa)', 'isobaricInhPa'), ('Unknown', 'unknown')],
        'st': [('At A Depth Below Land Layer', 'depthBelowLandLayer')],
        'soilw': [('At A Depth Below Land Layer', 'depthBelowLandLayer')],
        '2t': [('At A Height Above Ground', 'heightAboveGround')],
        'q': [('At A Height Above Ground', 'heightAboveGround'),
              ('Pressure From Ground Layer', 'pressureFromGroundLayer')],
        '2d': [('At A Height Above Ground', 'heightAboveGround')],
        '2r': [('At A Height Above Ground', 'heightAboveGround')],
        'aptmp': [('At A Height Above Ground', 'heightAboveGround')],
        'tmax': [('At A Height Above Ground', 'heightAboveGround')],
        'tmin': [('At A Height Above Ground', 'heightAboveGround')],
        '10u': [('At A Height Above Ground', 'heightAboveGround')],
        '10v': [('At A Height Above Ground', 'heightAboveGround')],
        'u': [('At A Height Above Ground', 'heightAboveGround'), ('At A Height Above the Sea', 'heightAboveSea'),
              ('Isobaric (hPa)', 'isobaricInhPa'), ('Max Wind', 'maxWind'),
              ('Potential Vorticity', 'potentialVorticity'),
              ('Pressure From Ground Layer', 'pressureFromGroundLayer'), ('Sigma', 'sigma'),
              ('Tropopause', 'tropopause'), ('Unknown', 'unknown')],
        'v': [('At A Height Above Ground', 'heightAboveGround'), ('At A Height Above the Sea', 'heightAboveSea'),
              ('Isobaric (hPa)', 'isobaricInhPa'), ('Max Wind', 'maxWind'),
              ('Potential Vorticity', 'potentialVorticity'),
              ('Pressure From Ground Layer', 'pressureFromGroundLayer'), ('Sigma', 'sigma'),
              ('Tropopause', 'tropopause'), ('Unknown', 'unknown')],
        't': [('At A Height Above Ground', 'heightAboveGround'), ('At A Height Above the Sea', 'heightAboveSea'),
              ('Isobaric (Pa)', 'isobaricInPa'), ('Isobaric (hPa)', 'isobaricInhPa'), ('Max Wind', 'maxWind'),
              ('Potential Vorticity', 'potentialVorticity'),
              ('Pressure From Ground Layer', 'pressureFromGroundLayer'), ('Sigma', 'sigma'), ('Surface', 'surface'),
              ('Tropopause', 'tropopause'), ('Unknown', 'unknown')],
        'pres': [('At A Height Above Ground', 'heightAboveGround'), ('Max Wind', 'maxWind'),
                 ('Potential Vorticity', 'potentialVorticity'), ('Tropopause', 'tropopause'), ('Unknown', 'unknown')],
        '100u': [('At A Height Above Ground', 'heightAboveGround')],
        '100v': [('At A Height Above Ground', 'heightAboveGround')],
        'hlcy': [('At A Height Above Ground Layer', 'heightAboveGroundLayer')],
        'ustm': [('At A Height Above Ground Layer', 'heightAboveGroundLayer')],
        'vstm': [('At A Height Above Ground Layer', 'heightAboveGroundLayer')],
        'clwmr': [('Hybrid Level', 'hybrid'), ('Isobaric (hPa)', 'isobaricInhPa')],
        'icmr': [('Hybrid Level', 'hybrid'), ('Isobaric (hPa)', 'isobaricInhPa')],
        'rwmr': [('Hybrid Level', 'hybrid'), ('Isobaric (hPa)', 'isobaricInhPa')],
        'snmr': [('Hybrid Level', 'hybrid'), ('Isobaric (hPa)', 'isobaricInhPa')],
        'grle': [('Hybrid Level', 'hybrid'), ('Isobaric (hPa)', 'isobaricInhPa')],
        'gh': [('Isothermal (0 Celcius)', 'isothermZero'), ('Isobaric (Pa)', 'isobaricInPa'),
               ('Isobaric (hPa)', 'isobaricInhPa'), ('Max Wind', 'maxWind'),
               ('Potential Vorticity', 'potentialVorticity'), ('Tropopause', 'tropopause'),
               ('Unknown', 'unknown')],
        'r': [('Isothermal (0 Celcius)', 'isothermZero'), ('Isobaric (hPa)', 'isobaricInhPa'),
              ('Pressure From Ground Layer', 'pressureFromGroundLayer'), ('Sigma', 'sigma'),
              ('Sigma Layer', 'sigmaLayer'), ('Unknown', 'unknown')],
        'absv': [('Isobaric (Pa)', 'isobaricInPa'), ('Isobaric (hPa)', 'isobaricInhPa')],
        'o3mr': [('Isobaric (Pa)', 'isobaricInPa'), ('Isobaric (hPa)', 'isobaricInhPa')],
        'w': [('Isobaric (hPa)', 'isobaricInhPa'), ('Sigma', 'sigma')],
        'wz': [('Isobaric (hPa)', 'isobaricInhPa')],
        'ICSEV': [('Isobaric (hPa)', 'isobaricInhPa')],
        '5wavh': [('Isobaric (hPa)', 'isobaricInhPa')],
        'icaht': [('Max Wind', 'maxWind'), ('Tropopause', 'tropopause')],
        'mslet': [('Mean Sea Level', 'meanSea')],
        'prmsl': [('Mean Sea Level', 'meanSea')],
        'uswrf': [('Nominal Top', 'nominalTop'), ('Surface', 'surface')],
        'ulwrf': [('Nominal Top', 'nominalTop'), ('Surface', 'surface')],
        'vwsh': [('Potential Vorticity', 'potentialVorticity'), ('Tropopause', 'tropopause')],
        'cape': [('Pressure From Ground Layer', 'pressureFromGroundLayer'), ('Surface', 'surface')],
        'cin': [('Pressure From Ground Layer', 'pressureFromGroundLayer'), ('Surface', 'surface')],
        'plpl': [('Pressure From Ground Layer', 'pressureFromGroundLayer')],
        'pt': [('Sigma', 'sigma')], 'vis': [('Surface', 'surface')], 'gust': [('Surface', 'surface')],
        'hindex': [('Surface', 'surface')], 'sp': [('Surface', 'surface')], 'orog': [('Surface', 'surface')],
        'sdwe': [('Surface', 'surface')], 'sde': [('Surface', 'surface')], 'pevpr': [('Surface', 'surface')],
        'cpofp': [('Surface', 'surface')], 'cprat': [('Surface', 'surface')], 'prate': [('Surface', 'surface')],
        'tp': [('Surface', 'surface')], 'acpcp': [('Surface', 'surface')], 'watr': [('Surface', 'surface')],
        'csnow': [('Surface', 'surface')], 'cicep': [('Surface', 'surface')], 'cfrzr': [('Surface', 'surface')],
        'crain': [('Surface', 'surface')], 'lhtfl': [('Surface', 'surface')], 'shtfl': [('Surface', 'surface')],
        'gflux': [('Surface', 'surface')], 'uflx': [('Surface', 'surface')], 'vflx': [('Surface', 'surface')],
        'u-gwd': [('Surface', 'surface')], 'v-gwd': [('Surface', 'surface')], 'wilt': [('Surface', 'surface')],
        'fldcp': [('Surface', 'surface')], 'SUNSD': [('Surface', 'surface')],'lftx': [('Surface', 'surface')],
        'dswrf': [('Surface', 'surface')], 'dlwrf': [('Surface', 'surface')], '4lftx': [('Surface', 'surface')],
        'hpbl': [('Surface', 'surface')], 'lsm': [('Surface', 'surface')], 'ci': [('Surface', 'surface')],
        'al': [('Surface', 'surface')], 'VRATE': [('Unknown', 'unknown')], 'pwat': [('Unknown', 'unknown')],
        'cwat': [('Unknown', 'unknown')], 'tozne': [('Unknown', 'unknown')], 'cwork': [('Unknown', 'unknown')]
    }
