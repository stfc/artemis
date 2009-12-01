<?php
#
#  Copyright Science and Technology Facilities Council, 2009.
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
#  $Revision$
#  $Date$
#  $LastChangedBy$
#

$RRD_DIR = "rrds/";

$DATE_FORMAT = "Y-m-d H:i:s";

  require('functions.php');

  //We need to masquerade as an image of the png variety
  ob_start();
  header("Content-type: image/png");
  ob_end_clean();
  session_write_close();

  //Get list of probe ids to graph
  if (isset($_REQUEST['ids']) && strlen($_REQUEST['ids']) > 0) {
    $ids = $_REQUEST['ids'];
    $ids = split(',', $ids); //arrays are better than comma seperated strings :-P
  }
  else {
    readfile("icons/status/image-missing.png");
    exit();
  }

  //Time range of graph
  $range = null;

  //Casting the timestamps as integers is my lazy form of input validation
  //Get start timestamp and check validity, abort nicely if bad
  if (isset($_GET['start'])) {
    $t_start = (int) $_GET['start'];
    $range .= "-s $t_start ";
  }
  else {
    readfile("icons/status/dialog-error.png");
    exit();
  }

  //Get end timestamp and check validity, abort nicely if bad
  if (isset($_GET['end'])) {
    $t_end = (int) $_GET['end'];
    $range .= "-e $t_end ";
  }
  else {
    readfile("icons/status/dialog-warning.png");
    exit();
  }

  //Abort if start is before or the same as end
  if ($t_start >= $t_end) {
    readfile("icons/status/image-loading.png");
    exit();
  }

  if (isset($_GET['mode'])) {
    $mode = $_GET['mode'];
  }
  else {
    $mode = null;
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
    $defs .= " DEF:$base_id=$base_rrd:temp:AVERAGE";
    $colour = array_shift($colours);
    $defs .= " HRULE:0#$colour$alpha:'$base_id\t (Baseline Probe)\\n'";
  }
  else {
    $base_id = null;
  }

  foreach ($ids as $i => $id) {
    $label = $id;
    $rrd="$RRD_DIR$id.rrd";  //datasource
    $colour=$colours[$i]; //grab colour
    //describe each probe's graph drawing here
    $defs .= " DEF:$id=$rrd:temp:AVERAGE";

    //Apply baseline if present
    if ($base_id != null) {
      $defs .= " CDEF:$id-norm=$id,$base_id,-";
      $id = $id."-norm";
    }

    //Calculate trend line
    if (strpos($id, 'AIRFLOW') !== false) {
      $defs .= " CDEF:$id-holder=$id,10,/";
      $defs .= " CDEF:$id-trend=$id-holder,$window,TREND";
    }
    else {
      $defs .= " CDEF:$id-trend=$id,$window,TREND";
    }

    $id = $id."-trend";

    //Plot line
    $defs .= " LINE:$id#$colour$alpha:'$label\t'";

    //Min & Max
    $defs .= " GPRINT:$id:MIN:'Min\: %.0lf\t'";
    $defs .= " GPRINT:$id:MAX:'Max\: %.0lf\\n'";

    //Draw nodata markers
    $defs .= " CDEF:$id-nodata=$id,UN,$j,*,2,/";
    $defs .= " AREA:$id-nodata#7F7F7F7F";

    $j--;
  }

  //draw the graph to stdout, which is this page :P
  $cmd= ("rrdtool graph - "
        ." -a PNG"               //Output type
        ." -c BACK#ffffff00"       //Background colour
        ." -c CANVAS#ffffff00"     //Graph Background colour
        ." -c SHADEA#ffffff00"     //Top and left shade
        ." -c SHADEB#ffffff00"     //Bottom and right shade
        ." -c FONT#003153"       //Font colour
        ." -c AXIS#2e3436"       //Axis colour
        ." -c ARROW#2e3436"      //Axis arrow colour
        ." -c MGRID#d3d7cf55"      //Major grid colour
        ." -c GRID#eeeeec33"     //Minor grid colour
        ." -c FRAME#2e3436"      //Frame colour
#        ." -t '"/*.date($DATE_FORMAT, $start)*/."2008-08-08 23:23 to 34538945'"
#       ." -E"                   //Sloping edges
        ." -h 480"               //Height
        ." -w 480"               //Width
        ." -u 60"                //Upper limit of graph
        ." -l 0"                 //Lower limit of graph
        ." $range"               //Time range
        ." -v 'Temperature (C)  Airflow (%/10)  Current(A)'" //Vertical axis label
#        ." --right-axis 1:0" //Vertical axis label
#        ." --right-axis-label 'Airflow (%)'" //Vertical axis label
        ."$defs"); 

  if ($mode == null) {
    $cmd .= " -r"; //Rigid limits
  }

  //execute
  system($cmd);
?>
