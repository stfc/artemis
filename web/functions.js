const  style_highlight = "4px inset";

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
var pUpdate = null;
var divRoom = null;


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
  var start = document.getElementById('inputDateStart').value;
  var end   = document.getElementById('inputDateEnd').value;

  var baseline = document.getElementById('inputBaseline').checked;

  start = '&start='    + start;
  end   = '&end='      + end;

  mode = '';

  if (baseline) {
    mode  = '&mode=baseline';
  }

  //Update image, changing the date lets the browser know its a new image preloading prevents the annoying update flicker
  var imgNew = new Image();
  imgNew.src = 'drawgraph.php?d='+(new Date()).getTime()+'&ids='+ids+start+end+mode;
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


function callbackJSON(responseText)
{
  const tileSize = 16;
  const offset_x = 8;
  const offset_y = 4;

  var time_start = new Date();

  var a_probes = eval(responseText); //get probe data and eval into an array

  pUpdate.innerHTML += 'HTTP state changed<br />';

  if (a_probes != null) {
    pUpdate.innerHTML += 'Got probe data<br />';
    divRoom.innerHTML = null; //makes the display flash, less than optimal

    var unknown_count = 0;

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

      //Put unknown probes along bottom
      if ((p_w == 0) && (p_h == 0)) {
        p_w = 16;
        p_h = 16;
        p_y = -20;
        p_x = 48 + unknown_count * 32;
        unknown_count++;
      }
      else {
        //Improve readability of small probes
        if (p_w < 2) {
          p_value = Math.round(p_value);
        }

        //Convert units from tiles to pixels
        p_w = p_w * tileSize;  //probe width in pixels
        p_h = p_h * tileSize;  //probe height in pixels

        p_x = p_x * tileSize;  //x-position in pixels
        p_y = p_y * tileSize;  //y_position in pixels

        p_x =        p_x  - (p_w / 2) - tileSize;  //x position in pixels
        p_y = (544 - p_y) - (p_h / 2) + tileSize;  //y position in pixels

        //Apply offsets (top-left corner of floor)
        p_x = p_x + offset_x;
        p_y = p_y + offset_y;
      }

      //Scale text with probe
      p_f = Math.min(p_w, p_h) / 4 + 4;  //font size
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

      pUpdate.innerHTML += '.';
    }

    pUpdate.innerHTML += '<br />';

    updateHighlights();
    updateGraph();

    var time_end = new Date();

    var time_took = (time_end - time_start) / 1000;

    pUpdate.innerHTML += 'Update took ' + time_took + ' seconds<br />';
  }
}

function setupJSON()
{
  pUpdate = document.getElementById("update_time");
  divRoom = document.getElementById("divRoom");
  http_request = new XMLHttpRequest();
  http_request.onreadystatechange = stateJSON;
}

function stateJSON()
{
  if (http_request.readyState == 0) {
    pUpdate.innerHTML += 'HTTP request not initialized<br />';
  }
  else if (http_request.readyState == 1) {
    pUpdate.innerHTML += 'HTTP request set up<br />';
  }
  else if (http_request.readyState == 2) {
    pUpdate.innerHTML += 'HTTP request sent<br />';
  }
  else if (http_request.readyState == 3) {
    pUpdate.innerHTML += 'HTTP request in process<br />';
  }
  else if (http_request.readyState == 4) {
    pUpdate.innerHTML += 'HTTP request complete<br />';
    callbackJSON(http_request.responseText);
  }
}

function updateProbesJSON()
{
  //Called periodically to refresh the sensor data
  pUpdate.innerHTML = 'Making HTTP request<br />';

  http_request.open('GET', './data/probe-data.json', true);
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
  else if (theme == "AIRFLOW") {
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
  else if (theme == "CURRENT") {
    r = 255;
    g = 127 + Math.round(result / 2);
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
