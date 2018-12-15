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
        )

        return url_maps
