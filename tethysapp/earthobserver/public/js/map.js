// Getting the csrf token
let csrftoken = Cookies.get('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

////////////////////////////////////////////////////////////////////////  LOAD THE MAP
// threddsbase and geoserverbase are defined in the base.html scripts sections
const mapObj = map();                   // used by legend and draw controls
const basemapObj = basemaps();          // used in the make controls function

////////////////////////////////////////////////////////////////////////  DRAWING/LAYER CONTROLS, MAP EVENTS, LEGEND
let drawnItems = new L.FeatureGroup().addTo(mapObj);      // FeatureGroup is to store editable layers
let drawControl = new L.Control.Draw({
    edit: {
        featureGroup: drawnItems,
        edit: false,
    },
    draw: {
        polyline: false,
        circlemarker: false,
        circle: false,
        polygon: false,
        rectangle: true,
    },
});
mapObj.addControl(drawControl);
mapObj.on("draw:drawstart ", function () {     // control what happens when the user draws things on the map
    drawnItems.clearLayers();
});
mapObj.on(L.Draw.Event.CREATED, function (event) {
    drawnItems.addLayer(event.layer);
    L.Draw.Event.STOP;
    getDrawnChart(drawnItems);
});

mapObj.on("mousemove", function (event) {
    $("#mouse-position").html('Lat: ' + event.latlng.lat.toFixed(5) + ', Lon: ' + event.latlng.lng.toFixed(5));
});

let layerObj = newLayer();              // adds the wms raster layer
let controlsObj = makeControls();       // the layer toggle controls top-right corner
legend.addTo(mapObj);                   // add the legend graphic to the map
latlon.addTo(mapObj);                   // add the box showing lat and lon to the map
updateGEOJSON();                        // asynchronously get geoserver wfs/geojson data for the regions

////////////////////////////////////////////////////////////////////////  EVENT LISTENERS
function update() {
    for (let i = 0; i < geojsons.length; i++) {
        geojsons[i][0].addTo(mapObj)
    }
    layerObj = newLayer();
    controlsObj = makeControls();
    getDrawnChart(drawnItems);
    legend.addTo(mapObj);
}

$("#model").change(function () {
    let model = $(this).val();
    if (model === 'gldas') {
        $("#gldascontrols").css({'display':'initial'});
        $("#gfscontrols").css({'display':'none'});
    } else if (model === 'gfs') {
        $("#gldascontrols").css({'display':'none'});
        $("#gfscontrols").css({'display':'initial'});
    }
    clearMap();
    update();
});

$("#gldas_vars").change(function () {
    clearMap();
    update();
});

$("#dates").change(function () {
    clearMap();
    update();
});

$("#gfs_vars").change(function () {
    clearMap();
    update();
});


$('#colorscheme').change(function () {
    clearMap();
    for (let i = 0; i < geojsons.length; i++) {
        geojsons[i][0].addTo(mapObj)
    }
    layerObj = newLayer();
    controlsObj = makeControls();
    legend.addTo(mapObj);
});

$("#opacity").change(function () {
    layerObj.setOpacity($(this).val());
});


$('#gjColor').change(function () {
    styleGeoJSON();
});
$("#gjOpacity").change(function () {
    styleGeoJSON();
});
$("#gjWeight").change(function () {
    styleGeoJSON();
});
$('#gjFillColor').change(function () {
    styleGeoJSON();
});
$("#gjFillOpacity").change(function () {
    styleGeoJSON();
});


$('#charttype').change(function () {
    makechart();
});
$("#display").click(function() {
    $("#displayopts").toggle();
});