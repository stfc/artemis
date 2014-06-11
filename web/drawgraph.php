<?php
#
#  Copyright Science and Technology Facilities Council, 2009-2012
#
#  This file is part of ARTEMIS.
#
#  ARTEMIS is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  ARTEMIS is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with ARTEMIS. If not, see <http://www.gnu.org/licenses/>.
#

  $RRD_DIR = "../rrds/";
  $DATE_FORMAT = "Y-m-d H:i:s";

  $run_mode = "web";
  if (isset($_SERVER["TERM"]) or isset($_REQUEST["debug"])) {
    $run_mode = "cli";
  }
  elseif (isset($_REQUEST["meta"])) {
    $run_mode = "meta";
  }

  require('functions.php');

  if ($run_mode == "web") {
    //We need to masquerade as an image of the png variety
    ob_start();
    header("Content-type: image/png");
    ob_end_clean();
    session_write_close();
  }
  else {
    ob_start();
    header("Content-type: text/plain");
    ob_end_clean();
    session_write_close();
  }


  //Get list of probe ids to graph
  if (isset($_REQUEST['ids']) && strlen($_REQUEST['ids']) > 0) {
    $ids = $_REQUEST['ids'];
    $ids = split(',', $ids); //arrays are better than comma seperated strings :-P
  }
  else {
    if ($run_mode == "web") {
      readfile("images/select.png");
    }
    else {
      echo "No probes specified";
    }
    exit();
  }

  //Time range of graph
  $range = null;

  //Get start timestamp and check validity, abort nicely if bad
  if (isset($_GET['start'])) {
    $t_start = preg_replace("/[^a-zA-Z0-9.]/", "", $_GET['start']);
    $range .= "-s $t_start ";
  }
  else {
    if ($run_mode == "web") {
      readfile("images/dialog-error.png");
    }
    else {
      echo "Start time not specified";
    }
    exit();
  }

  //Get end timestamp and check validity, abort nicely if bad
  if (isset($_GET['end'])) {
    $t_end = preg_replace("/[^a-zA-Z0-9.]/", "", $_GET['end']);
    $range .= "-e $t_end ";
  }
  else {
    if ($run_mode == "web") {
      readfile("images/dialog-warning.png");
    }
    else {
      echo "Start time not specified";
    }
    exit();
  }

  //Abort if start is before or the same as end
  if ($t_start >= $t_end) {
    if ($run_mode == "web") {
      readfile("images/image-loading.png");
    }
    else {
      echo "Time range inverted";
    }
    exit();
  }

  if (isset($_GET['mode'])) {
    $mode = $_GET['mode'];
  }
  else {
    $mode = null;
  }

  $trend = false;

  if (isset($_GET['trend'])) {
    $trend = true;
  }

  $width = 300;

  if (isset($_GET['width'])) {
    $width = $_GET['width'];
  }

  $height = 480;

  if (isset($_GET['height'])) {
    $height = $_GET['height'];
  }

  //other usefuls
  $colours = array(
    'cc0000',
    '73d216',
    '3465a4',
    'f57900',
    '75507b',
    'edd400'
  );
  $alpha = 'dd';

  //Trend window size, based on size of view
  $window = round(($t_end - $t_start) / 120);

  $defs = null; //need this later to build the graph definitions

  $j = sizeof($ids);

  if ($mode == "baseline") {
    $base_id = array_shift($ids);
    $base_rrd="$RRD_DIR$base_id.rrd";
    $defs .= " DEF:$base_id=$base_rrd:val:AVERAGE";
    $colour = array_shift($colours);
    $defs .= " HRULE:0#$colour$alpha:'$base_id\t<b>(Baseline Probe)</b>\\n'";
  }
  else {
    $base_id = null;
  }

  foreach ($ids as $i => $id) {
    $label = $id;
    $id_origin = $id;

    $rrd="$RRD_DIR$id.rrd";  //datasource
    $colour=$colours[$i]; //grab colour
    //describe each probe's graph drawing here
    $defs .= " DEF:$id=$rrd:val:AVERAGE";

    //Apply baseline if present
    if ($base_id != null) {
      $defs .= " CDEF:$id-norm=$id,$base_id,-";
      $id = $id."-norm";
    }

    //Scale airflow and humidity sensors
    if ((strpos($id, 'AIRFLOW') !== false) or (strpos($id, 'HUMIDITY') !== false)) {
      $defs .= " CDEF:$id-scaled=$id,2,/";
      $id .= "-scaled";
    }

    //Use trendline?
    if ($trend) {
      //Calculate trend line
      $defs .= " CDEF:$id-trend=$id,$window,TREND";

      //Switch to trendline
      $id .= "-trend";
    }

    //Plot line
    $defs .= " LINE:$id#$colour$alpha:'$label\t'";

    //Experimental rate of change line
    $defs .= " CDEF:$id-prev=$id,PREV\($id\),-";
#    $defs .= " CDEF:$id-prev=$id,PREV\($id\),-";
    $defs .= " CDEF:$id-prevh=$id-prev,1,GT";
    $defs .= " CDEF:$id-prevu=$id-prev,-1,LT";
    $defs .= " CDEF:$id-preva=$id-prev,ABS";
    $defs .= " AREA:$id-preva#00000055";
    $defs .= " TICK:$id-prevh#ff000033:1";
    $defs .= " TICK:$id-prevu#0000ff33:1";

    //Min & Max
    $defs .= " GPRINT:$id_origin:LAST:'<b>Now</b>\: %.2lf\t'";
    $defs .= " GPRINT:$id_origin:AVERAGE:'<b>Mean</b>\: %.2lf\t'";
    $defs .= " GPRINT:$id_origin:MIN:'<b>Min</b>\: %.2lf\t'";
    $defs .= " GPRINT:$id_origin:MAX:'<b>Max</b>\: %.2lf\\n'";

    //Draw nodata markers
    $defs .= " CDEF:$id-nodata=$id,UN,$j,*,2,/";
    $defs .= " AREA:$id-nodata#7F7F7F7F";

    $j--;
  }

  //draw the graph to stdout, which is this page :P
  $cmd= ("rrdtool graphv - "
    ." -a PNG"                 //Output as an PNG Image
    ." --pango-markup"         //Render text with Pango
    ." -R light"               //Slight hinting and anti-aliasing
    ." -T 64"                  //Set tabstop width
    ." -n AXIS:8:Helvetica"
    ." -n UNIT:8:Helvetica"
    ." -n LEGEND:7:Helvetica"
    ." -c BACK#ffffff"       //Background colour
    ." -c CANVAS#ffffff"     //Graph Background colour
    ." -c SHADEA#ffffff"     //Top and left shade
    ." -c SHADEB#ffffff"     //Bottom and right shade
    ." -c FONT#2e3436"       //Font colour
    ." -c AXIS#2e3436"       //Axis colour
    ." -c ARROW#2e3436"      //Axis arrow colour
    ." -c MGRID#babdb6"      //Major grid colour
    ." -c GRID#babdb6"       //Minor grid colour
    ." -c FRAME#2e3436"      //Frame colour
    ." -w $width"            //Width
    ." -h $height"           //Height
    ." --full-size-mode"     //Specify image size
    ." -u 50"                //Upper limit of graph
    ." -l 0"                 //Lower limit of graph
    ." $range"               //Time range
    ." -v '<b>Temperature</b> °C        <b>Current</b> A'" //Left Vertical axis label
    ." --right-axis 2:0"     //Right Vertical axis
    ." --right-axis-label '<b>Airflow</b> %        <b>Humidity</b> %'" //Right Vertical axis label
    ."$defs");

  if ($mode == null) {
    $cmd .= " -r"; //Rigid limits
  }
  $cmd .= " -E"; //Sloping edges

  //execute
  $imgdata = shell_exec($cmd);

  if ($run_mode == 'meta') {
    $data = preg_split("/BLOB_SIZE:[0-9]+\n/", $imgdata);
    $data = explode("\n", $data[0]);
    $meta = Array();
    foreach ($data as $i => $d) {
      $d = explode(" = ", $d);
      if ($d[0] != "image") {
        $meta[$d[0]] = (float)$d[1];
      }
    }
    echo json_encode($meta);
  }
  else {
    $d = preg_split("/BLOB_SIZE:[0-9]+\n/", $imgdata);
    echo $d[1];
  }
?>
