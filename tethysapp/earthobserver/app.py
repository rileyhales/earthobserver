from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.app_settings import CustomSetting

# todo verify that the gldas shell works without credentials
# todo add controls/page for running the data updating scripts
# todo write about the different EO models


class Earthobserver(TethysAppBase):
    """
    Tethys app class for Earth Observer Tool.
    """
    name = 'Earth Observer Tool'
    index = 'earthobserver:home'
    icon = 'earthobserver/images/globe.png'
    package = 'earthobserver'
    root_url = 'earthobserver'
    color = '#002366'
    description = 'A tethys app for visualizing Earth Observation (EO) products including GLDAS and GFS.\n' \
                  'View time-animated maps, generate charts of data, extract and download time series data ' \
                  'at a point, in a bounding box, or in a shapefile\n'
    tags = 'Earth Observations, Time Series, Maps, Charts, Downloads'
    enable_feedback = False
    feedback_emails = []
    version = 'Development - 3 July 2019'

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
                name='manage',
                url='earthobserver/manage',
                controller='earthobserver.controllers.manage'
            ),

            # url maps for ajax calls
            urlmap(
                name='getPointSeries',
                url='earthobserver/ajax/getPointSeries',
                controller='earthobserver.ajax.get_pointseries',
            ),
            urlmap(
                name='getPolygonAverage',
                url='earthobserver/ajax/getPolygonAverage',
                controller='earthobserver.ajax.get_polygonaverage',
            ),
            urlmap(
                name='getShapeAverage',
                url='earthobserver/ajax/getShapeAverage',
                controller='earthobserver.ajax.get_shapeaverage',
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
