const style_highlight = "4px inset";

var ids = new Array();
var style_colours = new Array( //This is where our arbitary limitation comes from
  'cc0000',
  '73d216',
  '3465a4',
  'f57900',
  '75507b',
  'edd400'
);
var arbitary_limit = style_colours.length;
var http_request = null;
//var pUpdate = null;
var divRoom = null;
//var moving = null;
var zoom_start  = null;
var zoom_end    = null;
var graph_start = null;
var graph_end   = null;


function viewGraph(id)
{
  var bAdd = true; //Start by assuming we can add another probe

  for (i in ids) {
    if (ids[i] == id) {
      //Remove Highlight
      var probe = document.getElementById(ids[i]);
      probe.style.outline = null;
      //Remove from array and do not add again
      ids.splice(i,1);
      bAdd = false;

      updateHighlights();
    }
  }

  if ((bAdd) && (ids.length < arbitary_limit)) { //check the arbitary limitation
    //Add to array
    ids.push(id);

    updateHighlights();
  }

  updateGraph();
}


function updateGraph()
{
  if ((zoom_start != null) && (zoom_end != null)) {
    graph_start = zoom_start;
    graph_end   = zoom_end;
    zoom_start  = null;
    zoom_end    = null;
    document.getElementById('inputDateStart').value = graph_start;
    document.getElementById('inputDateEnd').value   = graph_end;
  }
  else {
    graph_start = parseFloat(document.getElementById('inputDateStart').value);
    graph_end   = parseFloat(document.getElementById('inputDateEnd').value);
  }

  var baseline = document.getElementById('inputBaseline').checked;
  var trend    = document.getElementById('inputTrend').checked;

  var start = '&start=' + graph_start;
  var end   = '&end='   + graph_end;

  var width = window.innerWidth - parseInt(document.getElementById('divRoom').style.width);
  if (width < 300) width = window.innerWidth; //No point trying to fit it in, so make it big.
  document.getElementById('divGraph').style.width = width - 32 + "px";
  width = '&width=' + (width - 32);

  var height = window.innerHeight - 128;
  height = '&height=' + height;

  var mode = '';

  if (baseline) {
    mode  = '&mode=baseline';
  }

  if (trend) {
    trend  = '&trend=true';
  }
  else {
    trend = '';
  }

  //Update image, changing the date lets the browser know its a new image preloading prevents the annoying update flicker
  var imgNew = new Image();
  imgNew.src = 'drawgraph.php?d='+(new Date()).getTime()+'&ids='+ids+start+end+mode+trend+width+height
  document.getElementById('imgGraph').src = imgNew.src;
}


function updateHighlights()
{
  //Re-apply highlights
  for (i in ids) {
    //Highlight
    var probe = document.getElementById(ids[i]);
    if (probe != null) {
      probe.style.outline = style_highlight + ' #' + style_colours[i];
      probe.style.z_index  = 1;
    }
  }
}

/*
function pickup(id)
{
  moving = id;
  pUpdate.innerHTML = 'Picked Up ' + moving;
}

function drop()
{
  if (moving != null) {
    pUpdate.innerHTML = 'Dropped ' + moving;
    moving = null;
  }
}

function move(event)
{
  if (moving != null) {
    m = document.getElementById(moving);
    m.style.left = event.clientX + "px";
    m.style.top = event.clientY + "px";
    pUpdate.innerHTML = 'Moved ' + moving;
  }
}
*/

function zoom(event)
{
  const min_x = 67;
  const min_y = 42;
  const max_x = 550;
  const max_y = 522;
  var range_x = max_x - min_x;
  var range_y = max_y - min_y;
  var graph_range = graph_end - graph_start;
  var graph_pos = null;

  x = event.layerX;
  y = event.layerY;

  img = document.getElementById('imgGraph');

  if ((x >= min_x) && (y >= min_y) && (x <= max_x) && (y <= max_y)) {
    x = x - min_x;
    graph_pos = Math.round(((x / range_x) * graph_range) + graph_start);

    if (event.type == "mousemove") {
      if ((zoom_start == null) && (zoom_end == null)) {
        img.style.cursor = "w-resize";
      }
      else if ((zoom_start != null) && (zoom_end == null)) {
        img.style.cursor = "e-resize";
      }
      else {
        img.style.cursor = "";
      }
    }
    else if (event.type == "mouseup") {
      if ((zoom_start == null) && (zoom_end == null)) {
        zoom_start = graph_pos;
      }
      else if ((zoom_start != null) && (zoom_end == null)) {
        zoom_end = graph_pos;
        updateGraph();
      }
    }
  }
  else {
    img.style.cursor = "";
  }
}

function zoom_calc()
{
  var graph_range = graph_end - graph_start;
  return Math.round(graph_range / 10);
}

function zoom_in()
{
  var zoom_step = zoom_calc();
  zoom_start = graph_start + zoom_step;
  zoom_end   = graph_end   - zoom_step;
  updateGraph();
}

function zoom_out()
{
  var zoom_step = zoom_calc();
  zoom_start = graph_start - zoom_step;
  zoom_end   = graph_end   + zoom_step;
  updateGraph();
}


function zoom_back()
{
  var zoom_step = zoom_calc();
  zoom_start = graph_start - zoom_step;
  zoom_end   = graph_end   - zoom_step;
  updateGraph();
}

function zoom_forward()
{
  var zoom_step = zoom_calc();
  zoom_start = graph_start + zoom_step;
  zoom_end   = graph_end   + zoom_step;
  updateGraph();
}

function zoom_reset()
{
  var ut = Math.floor(new Date().getTime()/1000)
  zoom_start = ut - 604800;
  zoom_end   = ut;
  updateGraph();
}

function callbackJSON(responseText)
{
  var tileSize = 16;
  var offset_x = 0;
  var offset_y = 0;

  var time_start = new Date();

  var a_data   = eval('(' + responseText + ')'); //get probe data and eval into an array
  var a_probes = a_data["probes"];

  var tileSize = a_data["config"]["tile_size"];
  var offset_x = a_data["config"]["offset_x"];
  var offset_y = a_data["config"]["offset_y"];

  if (a_probes != null) {
    //pUpdate.innerHTML += 'Got probe data<br />';
    divRoom.innerHTML = null; //makes the display flash, less than optimal

    var unknown_count = 0;

    var show_temperature = document.getElementById('inputTemperature').checked;
    var show_airflow     = document.getElementById('inputAirflow').checked;
    var show_humidity    = document.getElementById('inputHumidity').checked;
    var show_current     = document.getElementById('inputCurrent').checked;

    var room_width = parseInt(document.getElementById('divRoom').style.width);

    for (var i = 0; i < a_probes.length; i++) {
      var p_id    = a_probes[i][0]; //id
      var p_value = a_probes[i][1]; //value
      var p_alias = a_probes[i][2]; //friendly name
      var p_x     = a_probes[i][3]; //x position in tiles
      var p_y     = a_probes[i][4]; //y position in tiles
      var p_w     = a_probes[i][5]; //width in tiles
      var p_h     = a_probes[i][6]; //height in tiles
      var p_f     = 0;              //font size
      var p_m     = 0;              //internal font margin

      var type = p_id.split('-', 1)[0];

      if (((type == 'TEMPERATURE') && show_temperature) || ((type == 'AIRFLOW') && show_airflow) || ((type == 'HUMIDITY') && show_humidity) || ((type == 'CURRENT') && show_current)) {
        //Put unknown probes along top of room area
        if ((p_w == 0) && (p_h == 0)) {
          p_w =  24;
          p_h =  16;
          p_y = -20;
          p_x =  room_width - (unknown_count + 1)  * 24;
          unknown_count++;
        }
        else {
          //Convert units from tiles to pixels
          p_w = p_w * tileSize;  //probe width in pixels
          p_h = p_h * tileSize;  //probe height in pixels
  
          p_x = (p_x * tileSize) - (p_w / 2) - (tileSize / 2);  //x-position in pixels
          p_y = (p_y * tileSize) - (p_h / 2) - (tileSize / 2);  //y_position in pixels
  
          //Apply offsets (top-left corner of floor)
          p_x = p_x + offset_x;
          p_y = p_y + offset_y;
        }
  
        //Improve readability of probes
        p_value = String(Math.round(p_value));
  
        //Scale text with probe
        p_f = Math.max(6, Math.min(12, p_w / p_value.length));  //font size
        p_m = (p_h / 2) - (p_f / 2) - 1;    //margin is (half probe height, minus half font size, minus one)
  
  
        divRoom.innerHTML += '<div'
                           + ' id="' + p_id + '"'
                           + ' title="' + p_id + " - " + p_alias + '"'
                           + ' class="probe-' + type.toLowerCase() + '"'
                           + ' onclick="viewGraph(\'' + p_id + '\');"'
                           + ' style="'
                             + ' left: ' + p_x + 'px;'
                             + ' top: ' + p_y + 'px;'
                             + ' width: ' + p_w + 'px;'
                             + ' height: ' + p_h + 'px;'
                             + ' background-color: '+scaleColour(p_value, type)+';'
                           + ' ">'
                           + '<p'
                           + ' style="'
                             + ' font-size: ' + p_f + 'px;'
                             + ' margin-top: ' + p_m + 'px;'
                           + '">'+p_value+'</p>'
                           + '</div>';
      }
    }

    updateHighlights();
    updateGraph();

    var time_end = new Date();

    var time_took = (time_end - time_start) / 1000;
  }
}

function setupJSON()
{
  divRoom = document.getElementById("divRoom");
  http_request = XMLHttpRequest();
  http_request.onreadystatechange = stateJSON;
}

function stateJSON()
{
  if (http_request.readyState == 4) {
    callbackJSON(http_request.responseText);
  }
}

function updateProbesJSON()
{
  //Called periodically to refresh the sensor data
  http_request.open('GET', './data/data-dump.json', true);
  http_request.send(null);
}


function scaleColour(input, theme)
{
  var t = input;

  //range of input scale
  if (theme == "TEMPERATURE") {
    t_min = 15;
    t_max = 40;
  }
  else if ((theme == "AIRFLOW") || (theme == "HUMIDITY")){
    t_min = 0;
    t_max = 100;
  }
  else if (theme == "CURRENT") {
    t_min = 0;
    t_max = 16;
  }
  else {
    t_min = 0;
    t_max = 50;
  }

  //range of colour scale
  const c_min = 0;
  const c_max = 255;

  //Clip the temperature to the above range
  t = Math.max(t_min, t);
  t = Math.min(t_max, t);

  //Apply transformation
  var result = Math.round((((t - t_min) / (t_max - t_min)) * (c_max - c_min)) + c_min);

  if (theme == "TEMPERATURE") {
    r = result;
    g = 0;
    b = 255 - result;
  }
  else if (theme == "AIRFLOW") {
    r = 0;
    g = Math.round(result / 2);
    b = 0;
  }
  else if (theme == "HUMIDITY") {
    r = 0;
    g = 127 + Math.round(result / 2);
    b = 127 + Math.round(result / 2);
  }
  else if (theme == "CURRENT") {
    r = result;
    g = result;
    b = 0;
  }
  else {
    r = result;
    g = result;
    b = result;
  }

  var colour = 'rgb('+r+', '+g+', '+b+')';

  return colour;
}
