var $loading = $('#view-file-loading');

var base_layer = new ol.layer.Tile({
	source: new ol.source.BingMaps({
		key: 'eLVu8tDRPeQqmBlKAjcw~82nOqZJe2EpKmqd-kQrSmg~AocUZ43djJ-hMBHQdYDyMbT-Enfsk0mtUIGws1WeDuOvjY4EXCH-9OK3edNLDgkc',
		imagerySet: 'Road'
		//            imagerySet: 'AerialWithLabels'
	})
});

var streams = new ol.layer.Image({
	source: new ol.source.ImageWMS({
	//url: 'https://tethys-staging.byu.edu/geoserver/colombia_hydroviewer/wms?service=WMS&version=1.1.0&request=GetMap&layers=colombia_hydroviewer:south_america-colombia-drainage_line&styles=&bbox=-8848693.5569,-1734764.9334000014,-7068509.3666,1396062.1385999992&width=436&height=768&srs=EPSG:3857&format=application/openlayers',
	url: 'https://tethys-staging.byu.edu/geoserver/colombia_hydroviewer/wms',
	params: { 'LAYERS': 'south_america-colombia-drainage_line' },
	serverType: 'geoserver',
    crossOrigin: 'Anonymous'
	})
});

var stations = new ol.layer.Image({
	source: new ol.source.ImageWMS({
	//url: 'https://tethys-staging.byu.edu/geoserver/colombia_hydroviewer/wms?service=WMS&version=1.1.0&request=GetMap&layers=colombia_hydroviewer:FEWS_Stations_N&styles=&bbox=-78.66874999035203,-4.223749999626143,-67.4668705422863,11.522081930231478&width=546&height=768&srs=EPSG:4326&format=application/openlayers',
	url: 'https://tethys-staging.byu.edu/geoserver/colombia_hydroviewer/wms',
	params: { 'LAYERS': 'FEWS_Stations_N' },
	serverType: 'geoserver',
    crossOrigin: 'Anonymous'
	})
});

var feature_layer = stations;
var current_layer;

var map = new ol.Map({
	target: 'showMapView',
	layers: [base_layer, streams, stations],
	view: new ol.View({
		center: ol.proj.fromLonLat([-73.073215, 3.900749]),
		zoom: 5
	})
});

function get_realTimeObsDataH (stationcode, stationname) {
	$('#realTimeObsDataH-loading').removeClass('hidden');
    $.ajax({
        url: 'get-realTimeObsDataH',
        type: 'GET',
        data: {'stationcode' : stationcode, 'stationname': stationname},
        error: function () {
            $('#info').html('<p class="alert alert-danger" style="text-align: center"><strong>An unknown error occurred while retrieving the data</strong></p>');
            $('#info').removeClass('hidden');

            setTimeout(function () {
                $('#info').addClass('hidden')
            }, 5000);
        },
        success: function (data) {
            if (!data.error) {
                $('#realTimeObsDataH-loading').addClass('hidden');
                $('#dates').removeClass('hidden');
//                $('#obsdates').removeClass('hidden');
                $loading.addClass('hidden');
                $('#realTimeObsDataH-chart').removeClass('hidden');
                $('#realTimeObsDataH-chart').html(data);

                //resize main graph
                Plotly.Plots.resize($("#realTimeObsDataH-chart .js-plotly-plot")[0]);

                var params = {
                    stationcode: stationcode,
                    stationname: stationname,
                };

                $('#submit-download-realTimeObsDataH').attr({
                    target: '_blank',
                    href: 'download-realTimeObsDataH?' + jQuery.param(params)
                });

                 $('#download-realTimeObsDataH').removeClass('hidden');

            } else if (data.error) {
            	$('#info').html('<p class="alert alert-danger" style="text-align: center"><strong>An unknown error occurred while retrieving the Data</strong></p>');
            	$('#info').removeClass('hidden');

            	setTimeout(function() {
            		$('#info').addClass('hidden')
                }, 5000);

            } else {
            	$('#info').html('<p><strong>An unexplainable error occurred.</strong></p>').removeClass('hidden');
            }
        }
    });
};

function get_historicObsDataH (stationcode, stationname) {
	$('#historicObsDataH-loading').removeClass('hidden');
    $.ajax({
        url: 'get-historicObsDataH',
        type: 'GET',
        data: {'stationcode' : stationcode, 'stationname': stationname},
        error: function () {
            $('#info').html('<p class="alert alert-danger" style="text-align: center"><strong>An unknown error occurred while retrieving the data</strong></p>');
            $('#info').removeClass('hidden');

            setTimeout(function () {
                $('#info').addClass('hidden')
            }, 5000);
        },
        success: function (data) {
            if (!data.error) {
                $('#historicObsDataH-loading').addClass('hidden');
                $('#dates').removeClass('hidden');
//                $('#obsdates').removeClass('hidden');
                $loading.addClass('hidden');
                $('#historicObsDataH-chart').removeClass('hidden');
                $('#historicObsDataH-chart').html(data);

                //resize main graph
                Plotly.Plots.resize($("#historicObsDataH-chart .js-plotly-plot")[0]);

                var params = {
                    stationcode: stationcode,
                    stationname: stationname,
                };

                $('#submit-download-historicObsDataH').attr({
                    target: '_blank',
                    href: 'download-historicObsDataH?' + jQuery.param(params)
                });

                $('#download-historicObsDataH').removeClass('hidden');

            } else if (data.error) {
            	$('#info').html('<p class="alert alert-danger" style="text-align: center"><strong>An unknown error occurred while retrieving the Data</strong></p>');
            	$('#info').removeClass('hidden');

            	setTimeout(function() {
            		$('#info').addClass('hidden')
                }, 5000);

            } else {
            	$('#info').html('<p><strong>An unexplainable error occurred.</strong></p>').removeClass('hidden');
            }
        }
    });
};

map.on('pointermove', function(evt) {
	if (evt.dragging) {
		return;
	}
	var pixel = map.getEventPixel(evt.originalEvent);
	var hit = map.forEachLayerAtPixel(pixel, function(layer) {
		if (layer == feature_layer) {
			current_layer = layer;
			return true;
		}
	});
	map.getTargetElement().style.cursor = hit ? 'pointer' : '';
});

map.on("singleclick", function(evt) {

	if (map.getTargetElement().style.cursor == "pointer") {

		var view = map.getView();
		var viewResolution = view.getResolution();
		var wms_url = current_layer.getSource().getGetFeatureInfoUrl(evt.coordinate, viewResolution, view.getProjection(), { 'INFO_FORMAT': 'application/json' });

		if (wms_url) {

			$("#obsgraph").modal('show');
			$('#realTimeObsDataH-chart').addClass('hidden');
			$('#historicObsDataH-chart').addClass('hidden');
			$('#realTimeObsDataH-loading').removeClass('hidden');
			$('#historicObsDataH-loading').removeClass('hidden');
			$("#station-info").empty()
			$('#download_realTimeObsH').addClass('hidden');
			$('#download_historicObsH').addClass('hidden');

			$.ajax({
				type: "GET",
				url: wms_url,
				dataType: 'json',
				success: function (result) {
					stationcode = result["features"][0]["properties"]["id"];
					stationname = result["features"][0]["properties"]["nombre"];
					stationlongitude = result["features"][0]["properties"]["lng"];
					stationlatitude = result["features"][0]["properties"]["lat"];
					stream = result["features"][0]["properties"]["corriente"];
					$("#station-info").append('<h3 id="Station-Name-Tab">Current Station: '+ stationname
						+ '</h3><h5 id="Station-Code-Tab">Station Code: '
						+ stationcode + '</h3><h5 id="Latitude">Latitude: '
						+ stationlatitude + '</h3><h5 id="Latitude">Longitude: '
						+ stationlongitude+ '</h5><h5>Stream: '+ stream);
					get_realTimeObsDataH (stationcode, stationname)
					get_historicObsDataH (stationcode, stationname)
				}
			});
		}
	};
});

function resize_graphs() {
    $("#realTimeObsDataH_tab_link").click(function() {
        Plotly.Plots.resize($("#realTimeObsDataH-chart .js-plotly-plot")[0]);
    });
    $("#historicObsDataH_tab_link").click(function() {
        Plotly.Plots.resize($("#historicObsDataH-chart .js-plotly-plot")[0]);
    });
};