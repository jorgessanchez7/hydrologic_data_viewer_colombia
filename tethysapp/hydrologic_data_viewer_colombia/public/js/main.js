var map;

require([
    "esri/Map",
    "esri/layers/MapImageLayer",
    "esri/views/MapView",
    "dojo/domReady!"
    ], function (Map, MapImageLayer, MapView) {
        map = new Map ({
        basemap: "topo",
        });

    var fews_stations_H = new MapImageLayer({
        url: "https://tethys-staging.byu.edu/geoserver/colombia_hydroviewer/wms?service=WMS&version=1.1.0&request=GetMap&layers=colombia_hydroviewer:FEWS_Stations_N&styles=&bbox=-78.66874999035203,-4.223749999626143,-67.4668705422863,11.522081930231478&width=546&height=768&srs=EPSG:4326&format=application/openlayers"
    });

    map.layers.add(fews_stations_H)

    var view = new MapView ({
        container: "showMapView",
        map: map,
        center: [-73.073215, 3.900749],
        zoom: 5
	});

});