////////////////////////////////////////////////////////////////////////  MAP FUNCTIONS
function map() {
    // create the map
    return L.map('map', {
        zoom: 2,
        minZoom: 1.25,
        boxZoom: true,
        maxBounds: L.latLngBounds(L.latLng(-100.0, -270.0), L.latLng(100.0, 270.0)),
        center: [20, 0],
        timeDimension: true,
        timeDimensionControl: true,
        timeDimensionControlOptions: {
            position: "bottomleft",
            autoPlay: true,
            loopButton: true,
            backwardButton: true,
            forwardButton: true,
            timeSliderDragUpdate: true,
            minSpeed: 1,
            maxSpeed: 6,
            speedStep: 1,
        },
    });
}

function basemaps() {
    // create the basemap layers
    // let Esri_WorldImagery = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}');
    // let Esri_WorldTerrain = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/{z}/{y}/{x}', {maxZoom: 13});
    let Esri_WorldImagery = L.esri.basemapLayer('Imagery');
    let Esri_WorldTerrain = L.esri.basemapLayer('Terrain');
    let Esri_Imagery_Labels = L.esri.basemapLayer('ImageryLabels');
    return {
        "ESRI Imagery": L.layerGroup([Esri_WorldImagery, Esri_Imagery_Labels]).addTo(mapObj),
        "ESRI Terrain": L.layerGroup([Esri_WorldTerrain, Esri_Imagery_Labels])
    }
}

////////////////////////////////////////////////////////////////////////  WMS LAYERS
const bounds = {
    'gldas': {
        'Albedo_inst': '4,82',
        'AvgSurfT_inst': '226,319',
        'CanopInt_inst': '0,1',
        'ECanop_tavg': '0,143',
        'ESoil_tavg': '0,186',
        'Evap_tavg': '-1,1',
        'LWdown_f_tavg': '122,490',
        'Lwnet_tavg': '-161,46',
        'PotEvap_tavg': '-3,1001',
        'Psurf_f_inst': '47070,104635',
        'Qair_f_inst': '0,1',
        'Qg_tavg': '-31,44',
        'Qh_tavg': '-89,257',
        'Qle_tavg': '-3,232',
        'Qs_acc': '0,14',
        'Qsb_acc': '0,12',
        'Qsm_acc': '0,5',
        'Rainf_f_tavg': '0,1',
        'Rainf_tavg': '0,1',
        'RootMoist_inst': '2,923',
        'SWE_inst': '0,121743',
        'SWdown_f_tavg': '0,398',
        'SnowDepth_inst': '0,305',
        'Snowf_tavg': '0,1',
        'SoilTMP0_10cm_inst': '232,319',
        'Swnet_tavg': '0,347',
        'Tair_f_inst': '233,317',
        'Tveg_tavg': '0,167',
        'Wind_f_inst': '0,17'
    },
    'gfs': {
        'al': '0,88',
        '4lftx': '-16,29',
        'cfrzr': '0,1',
        'cicep': '0,0',
        'crain': '0,1',
        'csnow': '0,1',
        'cape': '0,4687',
        'cin': '-1128,1',
        'acpcp': '0,41',
        'cprat': '0,1',
        'dlwrf': '59,516',
        'dswrf': '0,981',
        'fldcp': '0,1',
        'landn': '0,1',
        'lsm': '0,1',
        'lhtfl': '-110,652',
        'v-gwd': '-17,15',
        'uflx': '-4,3',
        'vflx': '-3,4',
        'orog': '-237,6110',
        'cpofp': '-51,100',
        'hpbl': '16,6353',
        'pevpr': '-35,2065',
        'prate': '0,1',
        'siconc': '0,1',
        'shtfl': '-227,541',
        'sde': '0,3',
        'SUNSD': '0,21600',
        'lftx': '-13,45',
        'sp': '48173,103796',
        't': '203,350',
        'tp': '0,100',
        'ulwrf': '95,741',
        'uswrf': '0,765',
        'vis': '0,24100',
        'sdwe': '0,434',
        'watr': '0,44',
        'wilt': '0,1',
        'gust': '0,33',
        'u-gwd': '-7,7'
    }
};

function newLayer() {
    let model = $("#model").val();
    let wmsurl, layer;
    if (model === 'gldas') {
        wmsurl = threddsbase + 'gldas/' + $("#dates").val() + '.ncml';
        layer = $("#gldas_vars").val()
    } else if (model === 'gfs') {
        wmsurl = threddsbase + 'gfs/gfs.ncml';
        layer = $("#gfs_vars").val()
    }
    let wmsLayer = L.tileLayer.wms(wmsurl, {
        // version: '1.3.0',
        layers: layer,
        dimension: 'time',
        useCache: true,
        crossOrigin: false,
        format: 'image/png',
        transparent: true,
        opacity: $("#opacity_raster").val(),
        BGCOLOR: '0x000000',
        styles: 'boxfill/' + $('#colorscheme').val(),
        colorscalerange: bounds[model][layer],
    });

    return L.timeDimension.layer.wms(wmsLayer, {
        name: 'time',
        requestTimefromCapabilities: true,
        updateTimeDimension: true,
        updateTimeDimensionMode: 'replace',
        cache: 20,
    }).addTo(mapObj);
}

////////////////////////////////////////////////////////////////////////  LEGEND DEFINITIONS
let legend = L.control({position: 'topright'});
legend.onAdd = function () {
    let wmsurl, layer;
    let model = $("#model").val();
    if (model === 'gldas') {
        wmsurl = threddsbase + 'gldas/' + $("#dates").val() + '.ncml';
        layer = $("#gldas_vars").val()
    } else if (model === 'gfs') {
        wmsurl = threddsbase + 'gfs/gfs.ncml';
        layer = $("#gfs_vars").val()
    }
    let div = L.DomUtil.create('div', 'legend');
    let url = wmsurl + "?REQUEST=GetLegendGraphic&LAYER=" + layer + "&PALETTE=" + $('#colorscheme').val() + "&COLORSCALERANGE=" + bounds[model][layer];
    div.innerHTML = '<img src="' + url + '" alt="legend" style="width:100%; float:right;">';
    return div
};

let latlon = L.control({position: 'bottomleft'});
latlon.onAdd = function () {
    let div = L.DomUtil.create('div', 'well well-sm');
    div.innerHTML = '<div id="mouse-position" style="text-align: center"></div>';
    return div;
};
////////////////////////////////////////////////////////////////////////  GEOJSON LAYERS - GEOSERVER + WFS / GEOJSON
let currentregion = '';              // tracks which region is on the chart for updates not caused by the user picking a new region
function layerPopups(feature, layer) {
    let region = feature.properties.name;
    layer.bindPopup('<a class="btn btn-default" role="button" onclick="getShapeChart(' + "'" + region + "'" + ')">Get timeseries (average) for ' + region + '</a>');
}

// declare a placeholder layer for all the geojson layers you want to add
let jsonparams = {
    onEachFeature: layerPopups,
    style: {
        color: $("#gjColor").val(),
        opacity: $("#gjOpacity").val(),
        weight: $("#gjWeight").val(),
        fillColor: $("#gjFillColor").val(),
        fillOpacity: $("#gjFillOpacity").val()
    }
};
let africa = L.geoJSON(false, jsonparams);
let asia = L.geoJSON(false, jsonparams);
let australia = L.geoJSON(false, jsonparams);
let centralamerica = L.geoJSON(false, jsonparams);
let europe = L.geoJSON(false, jsonparams);
let middleeast = L.geoJSON(false, jsonparams);
let northamerica = L.geoJSON(false, jsonparams);
let southamerica = L.geoJSON(false, jsonparams);
// create this reference array that other functions will build on
const geojsons = [
    [africa, 'africa', africa_json],
    [asia, 'asia', asia_json],
    [australia, 'australia', australia_json],
    [centralamerica, 'centralamerica', centralamerica_json],
    [europe, 'europe', europe_json],
    [middleeast, 'middleeast', middleeast_json],
    [northamerica, 'northamerica', northamerica_json],
    [southamerica, 'southamerica', southamerica_json],
];

// gets the geojson layers from geoserver wfs and updates the layer
function getWFSData(geoserverlayer, leafletlayer) {
    // http://jsfiddle.net/1f2Lxey4/2/
    let parameters = L.Util.extend({
        service: 'WFS',
        version: '1.0.0',
        request: 'GetFeature',
        typeName: 'gldas:' + geoserverlayer,
        maxFeatures: 10000,
        outputFormat: 'application/json',
        parseResponse: 'getJson',
        srsName: 'EPSG:4326',
        crossOrigin: 'anonymous'
    });
    $.ajax({
        async: true,
        jsonp: false,
        url: geoserverbase + L.Util.getParamString(parameters),
        contentType: 'application/json',
        success: function (data) {
            leafletlayer.addData(data).addTo(mapObj);
        },
    });
}

function updateGEOJSON() {
    if (geoserverbase === 'geojson') {
        for (let i = 0; i < geojsons.length; i++) {
            geojsons[i][0].addData(geojsons[i][2]).addTo(mapObj);
        }
    } else {
        for (let i = 0; i < geojsons.length; i++) {
            getWFSData(geojsons[i][1], geojsons[i][0]);
        }
    }
}

function styleGeoJSON() {
    // determine the styling to apply
    let style = {
        color: $("#gjColor").val(),
        opacity: $("#gjOpacity").val(),
        weight: $("#gjWeight").val(),
        fillColor: $("#gjFillColor").val(),
        fillOpacity: $("#gjFillOpacity").val(),
    };
    // apply it to all the geojson layers
    for (let i = 0; i < geojsons.length; i++) {
        geojsons[i][0].setStyle(style);
    }
}

////////////////////////////////////////////////////////////////////////  MAP CONTROLS AND CLEARING
// the layers box on the top right of the map
function makeControls() {
    return L.control.layers(basemapObj, {
        'Earth Observation': layerObj,
        'Drawing': drawnItems,
        'Europe': europe,
        'Asia': asia,
        'Middle East': middleeast,
        'North America': northamerica,
        'Central America': centralamerica,
        'South America': southamerica,
        'Africa': africa,
        'Australia': australia,
    }).addTo(mapObj);
}

// you need to remove layers when you make changes so duplicates dont persist and accumulate
function clearMap() {
    // remove the controls for the wms layer then remove it from the map
    controlsObj.removeLayer(layerObj);
    mapObj.removeLayer(layerObj);
    // now do it for all the geojson layers
    for (let i = 0; i < geojsons.length; i++) {
        controlsObj.removeLayer(geojsons[i][0]);
        mapObj.removeLayer(geojsons[i][0]);
    }
    // now delete the controls object
    mapObj.removeControl(controlsObj);
}
