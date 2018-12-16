from tethys_sdk.base import TethysAppBase, url_map_maker


class HydrologicDataViewerColombia(TethysAppBase):
    """
    Tethys app class for Hydrologic Data Viewer Colombia.
    """

    name = 'Hydrologic Data Viewer Colombia'
    index = 'hydrologic_data_viewer_colombia:home'
    icon = 'hydrologic_data_viewer_colombia/images/colombia.png'
    package = 'hydrologic_data_viewer_colombia'
    root_url = 'hydrologic-data-viewer-colombia'
    color = '#00374b'
    description = 'This app shows the historical data for the Colombian Hydrologic Alert System of tThe Institute of Hydrology, Meteorology and Environmental Studies - IDEAM'
    tags = 'Hydrology'
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='home',
                url='hydrologic-data-viewer-colombia',
                controller='hydrologic_data_viewer_colombia.controllers.home'
            ),
            UrlMap(
                name='hobs',
                url='hydrologic-data-viewer-colombia/hobs',
                controller='hydrologic_data_viewer_colombia.controllers.hobs'
            ),
            UrlMap(
                name='hsen',
                url='hydrologic-data-viewer-colombia/hsen',
                controller='hydrologic_data_viewer_colombia.controllers.hsen'
            ),
            UrlMap(
                name='qobs',
                url='hydrologic-data-viewer-colombia/qobs',
                controller='hydrologic_data_viewer_colombia.controllers.qobs'
            ),
            UrlMap(
                name='qsen',
                url='hydrologic-data-viewer-colombia/qsen',
                controller='hydrologic_data_viewer_colombia.controllers.qsen'
            ),
            UrlMap(
                name='about',
                url='hydrologic-data-viewer-colombia/about',
                controller='hydrologic_data_viewer_colombia.controllers.about'
            ),
            UrlMap(
                name='get_realTimeObsDataH',
                url='hobs/get-realTimeObsDataH',
                controller='hydrologic_data_viewer_colombia.controllers.get_realTimeObsDataH'
            ),
            UrlMap(
                name='get_historicObsDataH',
                url='hobs/get-historicObsDataH',
                controller='hydrologic_data_viewer_colombia.controllers.get_historicObsDataH'
            ),
            UrlMap(
                name='download_realTimeObsDataH',
                url='hobs/download-realTimeObsDataH',
                controller='hydrologic_data_viewer_colombia.controllers.download_realTimeObsDataH'
            ),
            UrlMap(
                name='download_historicObsDataH',
                url='hobs/download-historicObsDataH',
                controller='hydrologic_data_viewer_colombia.controllers.download_historicObsDataH'
            ),
            UrlMap(
                name='get_realTimeSensorDataH',
                url='hsen/get-realTimeSensorDataH',
                controller='hydrologic_data_viewer_colombia.controllers.get_realTimeSensorDataH'
            ),
            UrlMap(
                name='get_historicSensorDataH',
                url='hsen/get-historicSensorDataH',
                controller='hydrologic_data_viewer_colombia.controllers.get_historicSensorDataH'
            ),
            UrlMap(
                name='download_realTimeSensorDataH',
                url='hsen/download-realTimeSensorDataH',
                controller='hydrologic_data_viewer_colombia.controllers.download_realTimeSensorDataH'
            ),
            UrlMap(
                name='download_historicSensorDataH',
                url='hsen/download-historicSensorDataH',
                controller='hydrologic_data_viewer_colombia.controllers.download_historicSensorDataH'
            ),
            UrlMap(
                name='get_realTimeObsDataQ',
                url='qobs/get-realTimeObsDataQ',
                controller='hydrologic_data_viewer_colombia.controllers.get_realTimeObsDataQ'
            ),
            UrlMap(
                name='get_historicObsDataQ',
                url='qobs/get-historicObsDataQ',
                controller='hydrologic_data_viewer_colombia.controllers.get_historicObsDataQ'
            ),
            UrlMap(
                name='download_realTimeObsDataQ',
                url='qobs/download-realTimeObsDataQ',
                controller='hydrologic_data_viewer_colombia.controllers.download_realTimeObsDataQ'
            ),
            UrlMap(
                name='download_historicObsDataQ',
                url='qobs/download-historicObsDataQ',
                controller='hydrologic_data_viewer_colombia.controllers.download_historicObsDataQ'
            ),
            UrlMap(
                name='get_realTimeSensorDataQ',
                url='qsen/get-realTimeSensorDataQ',
                controller='hydrologic_data_viewer_colombia.controllers.get_realTimeSensorDataQ'
            ),
            UrlMap(
                name='get_historicSensorDataQ',
                url='qsen/get-historicSensorDataQ',
                controller='hydrologic_data_viewer_colombia.controllers.get_historicSensorDataQ'
            ),
            UrlMap(
                name='download_realTimeSensorDataQ',
                url='qsen/download-realTimeSensorDataQ',
                controller='hydrologic_data_viewer_colombia.controllers.download_realTimeSensorDataQ'
            ),
            UrlMap(
                name='download_historicSensorDataQ',
                url='qsen/download-historicSensorDataQ',
                controller='hydrologic_data_viewer_colombia.controllers.download_historicSensorDataQ'
            ),
        )

        return url_maps
