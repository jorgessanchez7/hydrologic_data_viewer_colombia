from tethys_sdk.base import TethysAppBase, url_map_maker


class HydrologicDataViewerColombia(TethysAppBase):
    """
    Tethys app class for Hydrologic Data Viewer Colombia.
    """

    name = 'Hydrologic Data Viewer Colombia'
    index = 'hydrologic_data_viewer_colombia:home'
    icon = 'hydrologic_data_viewer_colombia/images/icon.gif'
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
        )

        return url_maps
