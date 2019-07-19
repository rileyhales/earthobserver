from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.app_settings import CustomSetting


class Earthobserver(TethysAppBase):
    """
    Tethys app class for Earth Observer Tool.
    """
    name = 'Earth Observer Tool'
    index = 'earthobserver:home'
    icon = 'earthobserver/images/observe.jpg'
    package = 'earthobserver'
    root_url = 'earthobserver'
    color = '#002366'
    description = 'A visualization tool for Earth Observation (EO) products including GLDAS and GFS. View ' \
                  'time-animated maps, generate and download charts of timeseries data at a point, in a bounding ' \
                  'box, or in a shapefile. Manages data downloading and updating workflows to keep EO data current.'
    tags = 'Earth Observations, Time Series, Maps, Charts, Downloads'
    enable_feedback = False
    feedback_emails = []
    version = 'Development - 8 July 2019'

    def url_maps(self):
        """
        Add controllers
        """
        urlmap = url_map_maker(self.root_url)

        url_maps = (
            # url maps to navigable pages
            urlmap(
                name='home',
                url='earthobserver',
                controller='earthobserver.controllers.home'
            ),
            urlmap(
                name='map',
                url='earthobserver/map',
                controller='earthobserver.controllers.map'
            ),
            urlmap(
                name='apihelp',
                url='earthobserver/apihelp',
                controller='earthobserver.controllers.apihelp'
            ),
            urlmap(
                name='data',
                url='earthobserver/data',
                controller='earthobserver.controllers.data'
            ),

            # url maps for data processing workflows
            urlmap(
                name='rungfs',
                url='earthobserver/workflows/rungfs',
                controller='earthobserver.controllers.rungfs',
            ),

            # url maps for ajax calls
            urlmap(
                name='getChart',
                url='earthobserver/ajax/getChart',
                controller='earthobserver.ajax.getchart',
            ),
            urlmap(
                name='uploadShapefile',
                url='earthobserver/ajax/uploadShapefile',
                controller='earthobserver.ajax.uploadshapefile',
            ),
            urlmap(
                name='getLevelsForVar',
                url='gfs/ajax/getLevelsForVar',
                controller='gfs.ajax.get_levels_for_variable'
            ),

            # url maps for api calls
            urlmap(
                name='getcapabilities',
                url='earthobserver/api/getcapabilities',
                controller='earthobserver.api.getcapabilities',
            ),
            urlmap(
                name='eodatamodels',
                url='earthobserver/api/eodatamodels',
                controller='earthobserver.api.eodatamodels',
            ),
            urlmap(
                name='timeseries',
                url='earthobserver/api/timeseries',
                controller='earthobserver.api.timeseries',
            ),
            urlmap(
                name='gldasvariables',
                url='earthobserver/api/gldasvariables',
                controller='earthobserver.api.gldasvariables',
            ),
            urlmap(
                name='gldasdates',
                url='earthobserver/api/gldasdates',
                controller='earthobserver.api.gldasdates',
            ),
            urlmap(
                name='gfslevels',
                url='earthobserver/api/gfslevels',
                controller='earthobserver.api.gfslevels',
            ),
            urlmap(
                name='gfsdates',
                url='earthobserver/api/gfsdates',
                controller='earthobserver.api.gfsdates',
            ),
        )
        return url_maps

    def custom_settings(self):
        custom_settings = (
            CustomSetting(
                name='Local Thredds Folder Path',
                type=CustomSetting.TYPE_STRING,
                description="Local file path to folder containing these datasets, same as is used by THREDDS "
                            "(e.g. /home/thredds/myDataFolder/)",
                required=True,
            ),
            CustomSetting(
                name='Thredds WMS URL',
                type=CustomSetting.TYPE_STRING,
                description="URL to the Earth Observer app's folder on the THREDDS server "
                            "(e.g. http://[host]/thredds/earthobserver/)",
                required=True,
            ),
            CustomSetting(
                name='Geoserver Workspace URL',
                type=CustomSetting.TYPE_STRING,
                description="WFS URL of the geoserver workspace containing the world region shapefiles for this app "
                            "(e.g. https://[host]/geoserver/earthobserver/ows)"
                            "Enter geojson instead of a url if you experience GeoServer problems.",
                required=True,
            ),
        )
        return custom_settings
