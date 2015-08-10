var displays_simulationSVG;
var displays_simulationSVGRoot;
var displays_colorPixelOn = "#c0ff00";
var displays_colorPixelOff = "#444444";
var displays_colorStopIndicatorOn = "#ff0000";
var displays_colorStopIndicatorOff = "#222222";
var powerState = false;

function displays_setPixel(row, col, state) {
    pixel = $("#pixel-" + row + "-" + col, displays_simulationSVGRoot);
    pixel.attr('fill', state ? displays_colorPixelOn : displays_colorPixelOff);
}

function displays_setStopIndicator(state) {
    indicator = $("#text-stop-indicator", displays_simulationSVGRoot);
    indicator.attr('fill', state ? displays_colorStopIndicatorOn : displays_colorStopIndicatorOff);
}

function displays_setBitmap(bitmap) {
    if(!bitmap) {
        return;
    }
    
    for(var row = 0; row < 8; row++) {
        for(var col = 0; col < 120; col++) {
            displays_setPixel(row, col, bitmap[row][col]);
        }
    }
}

function displays_clearBitmap() {
    for(var row = 0; row < 8; row++) {
        for(var col = 0; col < 120; col++) {
            displays_setPixel(row, col, false);
        }
    }
}

function displays_bitmapLoadCallback(response, status) {
    if(status == "success") {
        displays_setBitmap(response);
    }
}

function displays_statesLoadCallback(response, status) {
    if(status == "success") {
        displays_setStopIndicator(response['stop_indicator']);
        powerState = response['power_state'];
        if(!powerState) displays_clearBitmap();
    }
}

function displays_loadCurrentBitmap() {
    if(!powerState) return;
    var url = "bitmap.json";
    var ajax = $.ajax({
        type: "GET",
        url: url,
        timeout: 5000
    });
    
    // Register callback
    ajax.always(displays_bitmapLoadCallback);
}

function displays_loadStates() {
    var url = "states.json";
    var ajax = $.ajax({
        type: "GET",
        url: url,
        timeout: 5000
    });
    
    // Register callback
    ajax.always(displays_statesLoadCallback);
}

function displays_initSimulation() {
    $("#display-simulation").svg({
        loadURL: STATIC_PREFIX + "images/displays/display-simulation.svg"
    });
    displays_simulationSVG = $("#display-simulation").svg('get');
    displays_simulationSVGRoot = displays_simulationSVG.root();
    displays_loadStates();
    setTimeout(displays_loadCurrentBitmap, 500);
    setInterval(displays_loadCurrentBitmap, 3000);
    setInterval(displays_loadStates, 3000);
}

$(document).ready(displays_initSimulation);
