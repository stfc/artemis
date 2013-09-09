const style_highlight = "4px inset";

function map(x, in_min, in_max, out_min, out_max)
{
  return Math.round((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min);
}

function RGBColour(r, g ,b)
{
  this.r = r;
  this.g = g;
  this.b = b;

  this.hex = RGBColourToHex;
}

function RGBColourToHex()
{
  var result = "";
  var rgb = [this.r, this.g, this.b];

  for (i in rgb) {
    s = rgb[i].toString(16);

    while (s.length < 2) {
      s = "0" + s;
    }

    result = result + s;
  }
  return result;
}


function mapRGB(x, in_min, in_max, rgb_min, rgb_max)
{
  r = map(x, in_min, in_max, rgb_min.r, rgb_max.r);
  g = map(x, in_min, in_max, rgb_min.g, rgb_max.g);
  b = map(x, in_min, in_max, rgb_min.b, rgb_max.b);
  return new RGBColour(r,g,b);
}


//Tango Palette definition as RGBColours for later use
var Blue          = new RGBColour(  0,   0, 255);
var Green         = new RGBColour(  0, 255,   0);
var Red           = new RGBColour(255,   0,   0);

var Butter_1      = new RGBColour(252, 233,  79);
var Butter_2      = new RGBColour(237, 212,   0);
var Butter_3      = new RGBColour(196, 160,   0);
var Chameleon_1   = new RGBColour(138, 226,  52);
var Chameleon_2   = new RGBColour(115, 210,  22);
var Chameleon_3   = new RGBColour( 78, 154,   6);
var Orange_1      = new RGBColour(252, 175,  62);
var Orange_2      = new RGBColour(245, 121,   0);
var Orange_3      = new RGBColour(206,  92,   0);
var Sky_Blue_1    = new RGBColour(114, 159, 207);
var Sky_Blue_2    = new RGBColour( 52, 101, 164);
var Sky_Blue_3    = new RGBColour( 32,  74, 135);
var Plum_1        = new RGBColour(173, 127, 168);
var Plum_2        = new RGBColour(117,  80, 123);
var Plum_3        = new RGBColour( 92,  53, 102);
var Chocolate_1   = new RGBColour(233, 185, 110);
var Chocolate_2   = new RGBColour(193, 125,  17);
var Chocolate_3   = new RGBColour(143,  89,   2);
var Scarlet_Red_1 = new RGBColour(239,  41,  41);
var Scarlet_Red_2 = new RGBColour(204,   0,   0);
var Scarlet_Red_3 = new RGBColour(164,   0,   0);
var Aluminium_1   = new RGBColour(238, 238, 236);
var Aluminium_2   = new RGBColour(211, 215, 207);
var Aluminium_3   = new RGBColour(186, 189, 182);
var Aluminium_4   = new RGBColour(136, 138, 133);
var Aluminium_5   = new RGBColour( 85,  87,  83);
var Aluminium_6   = new RGBColour( 46,  52,  54);

var ids = new Array();
var meta = null;

var style_colours = new Array( //This is where our arbitary limitation comes from
  Scarlet_Red_2.hex(),
  Chameleon_2.hex(),
  Sky_Blue_2.hex(),
  Plum_2.hex(),
  Orange_2.hex(),
  Butter_2.hex()
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
    graph_start = document.getElementById('inputDateStart').value;
    graph_end   = document.getElementById('inputDateEnd').value;
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
  } else {
    trend = '';
  }

  //Update image, changing the date lets the browser know its a new image preloading prevents the annoying update flicker
  var src = 'drawgraph.php?d='+(new Date()).getTime()+'&ids='+ids+start+end+mode+trend+width+height;
  var metasrc = src + "&meta";
  $("#imgGraph").attr("src", src);
  $.getJSON(metasrc, function(stuff) {
    if (stuff != "No probes specified") {
      meta = stuff;
    }
  });
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

function callbackJSON(a_data)
{

  var tileSize = 16;
  var offset_x = 0;
  var offset_y = 0;

  var time_start = new Date();

  //var a_data   = eval('(' + responseText + ')'); //get probe data and eval into an array
  var a_probes = a_data["probes"];

  var tileSize = a_data["config"]["tile_size"];
  var offset_x = a_data["config"]["offset_x"];
  var offset_y = a_data["config"]["offset_y"];

  if (a_probes != null) {
    //pUpdate.innerHTML += 'Got probe data<br />';
    //divRoom.background = 'rooms/room.png?' + Math.Random();
    $("#divRoom").html(""); //makes the display flash, less than optimal

    var unknown_count = 0;

    var show_temperature = document.getElementById('inputTemperature').checked;
    var show_airflow     = document.getElementById('inputAirflow').checked;
    var show_humidity    = document.getElementById('inputHumidity').checked;
    var show_current     = document.getElementById('inputCurrent').checked;

    var room_width = parseInt(document.getElementById('divRoom').style.width);

    var h = "";

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
          p_y = -40;
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

        textColour = '#000';

        if (p_value > 35) {
          textColour = '#000';
        }
  
        h += '<div'
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
                             + ' color: '+textColour+';'
                           + ' ">'
                           + '<p'
                           + ' style="'
                             + ' font-size: ' + p_f + 'px;'
                             + ' margin-top: ' + p_m + 'px;'
                           + '">'+p_value+'</p>'
                           + '</div>';
      }
    }
    $("#divRoom").html(h)

    updateHighlights();
    updateGraph();

    var time_end = new Date();

    var time_took = (time_end - time_start) / 1000;
  }
}


function scaleColour(input, theme)
{
  var t = input;

  //range of input scale
  if (theme == "TEMPERATURE") {
    t_min = 15;
    t_max = 40;
    rgb_min = new RGBColour(  0,   0, 255);
    rgb_mid = new RGBColour(255,   0,   0);
    rgb_max = new RGBColour(255, 255,   0);
  }
  else {
    t_min = 0;
    t_max = 50;
    rgb_min = Aluminium_6;
    rgb_mid = Aluminium_3;
    rgb_max = Aluminium_1;
  }

  //Clip the temperature to the above range
  t = Math.max(t_min, t);
  t = Math.min(t_max, t);

  var t_mid = (t_max + t_min) / 2;

  //Apply transformation
  var result = mapRGB(t, t_min, t_mid, rgb_min, rgb_mid);
  if (t >= t_mid) {
    result = mapRGB(t, t_mid, t_max, rgb_mid, rgb_max);
  }
  var colour = 'rgb('+result.r+', '+result.g+', '+result.b+')';

  return colour;
}


function popupGraph(i) {
  u = i.src;
  w = window.open(u, "ARTEMIS", "width=1024,height=768,left=64,top=64,resizable=no,scrollbars=no,directories=no,titlebar=no,toolbar=no,status=no");
  w.window.focus();
}
