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
#  $Revision: 9149 $
#  $Date: 2011-09-28 14:31:59 +0100 (Wed, 28 Sep 2011) $
#  $LastChangedBy: tkk76468@FED.CCLRC.AC.UK $
#

  $RRD_DIR = "../rrds/";
  $DATE_FORMAT = "Y-m-d H:i:s";
  $DEFAULT_PERIOD = 720;
  $HORIZONTAL_MULTIPLIER = 60; //Seconds per pixel of horizontal resolution

  $run_mode = "web";
  if (isset($_SERVER["TERM"]) or isset($_REQUEST["debug"])) {
    $run_mode = "cli";
  }

  require('functions.php');

  if ($run_mode == "web") {
    //We need to masquerade as an image of the png variety
    ob_start();
    header("Content-type: image/png");
    #header("Content-type: text/plain");
    ob_end_clean();
    session_write_close();
  }

  //Get list of probe ids to graph
  $id = null;
  if (isset($_REQUEST['id']) && strlen($_REQUEST['id']) > 0) {
    $id = $_REQUEST['id'];
  }

  //Time range of graph
  $range = null;

  //Casting the timestamps as integers is my lazy form of input validation
  //Get start timestamp and check validity, abort nicely if bad
  if (isset($_GET['start'])) {
    $t_start = (int) $_GET['start'];
  }
  else {
    $t_start = (int) time() - $DEFAULT_PERIOD * $HORIZONTAL_MULTIPLIER;
  }

  //Get end timestamp and check validity, abort nicely if bad
  if (isset($_GET['end'])) {
    $t_end = (int) $_GET['end'];
  }
  else {
    $t_end = (int) time();
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

  $width = $DEFAULT_PERIOD;

  if (isset($_GET['width'])) {
    $width = $_GET['width'];
    $t_start = (int) time() - $width * $HORIZONTAL_MULTIPLIER;
  }

  $height = 200;

#  if (isset($_GET['height'])) {
#    $height = $_GET['height'];
#  }

  $show_bms = False;

  if (isset($_GET['bms'])) {
    $show_bms = True;
  }

  $range .= "-s $t_start ";
  $range .= "-e $t_end ";

  $defs = null; //need this later to build the graph definitions

  $rrd="$RRD_DIR$id.rrd";  //datasource

  //describe each probe's graph drawing here
  $defs .= " DEF:$id=$rrd:collect:AVERAGE";
  $defs .= " DEF:$id-min=$rrd:collect:MIN";
  $defs .= " DEF:$id-max=$rrd:collect:MAX";
  $defs .= " CDEF:$id-range=$id-max,$id-min,-";

  $defs .= " DEF:$id-nodes=$rrd:nodes:AVERAGE";
  $defs .= " DEF:$id-probes=$rrd:probes:AVERAGE";
  $defs .= " CDEF:$id-nodesx=$id-nodes,10,/";
  $defs .= " CDEF:$id-probesx=$id-probes,10,/";

  //Plot
  $defs .= " LINE:$id-min#3465a4:'Hourly Minimum\\t'";

  $defs .= " AREA:$id-range#d3d7df77::STACK";
  $defs .= " LINE:$id-max#cc0000:'Hourly Maximum\\l'";
  $defs .= " COMMENT:'\\s'";
  $defs .= " LINE:$id#2e3436:'Run Time\\t'";

  //Min & Max
  $defs .= " GPRINT:$id:LAST:'<b>Last Run</b>\: %-6.2lfs\\t'";
  $defs .= " GPRINT:$id:AVERAGE:'<b>Mean</b>\: %-6.2lfs\\t'";
  $defs .= " GPRINT:$id:MIN:'<b>Min</b>\: %-6.2lfs\\t'";
  $defs .= " GPRINT:$id:MAX:'<b>Max</b>\: %-6.2lfs\\l'";
  $defs .= " COMMENT:'\\s'";

  //Draw nodata markers
  $defs .= " CDEF:$id-nodata=$id,UN";
  $defs .= " TICK:$id-nodata#babdb677:1";

  //Operating Parameters
/*
  $defs .= " LINE2:$id-nodesx#f5750077:'Nodes\t'";
  $defs .= " GPRINT:$id-nodes:LAST:'<b>Last Run</b>\: %-8.0lf\\t'";
  $defs .= " GPRINT:$id-nodes:AVERAGE:'<b>Mean</b>\: %-8.0lf\\t'";
  $defs .= " GPRINT:$id-nodes:MIN:'<b>Min</b>\: %-8.0lf\\t'";
  $defs .= " GPRINT:$id-nodes:MAX:'<b>Max</b>\: %-8.0lf\\n'";

  $defs .= " LINE2:$id-probesx#73d21677:'Probes\\t'";
  $defs .= " GPRINT:$id-probes:LAST:'<b>Last Run</b>\: %-8.0lf\\t'";
  $defs .= " GPRINT:$id-probes:AVERAGE:'<b>Mean</b>\: %-8.0lf\\t'";
  $defs .= " GPRINT:$id-probes:MIN:'<b>Min</b>\: %-8.0lf\\t'";
  $defs .= " GPRINT:$id-probes:MAX:'<b>Max</b>\: %-8.0lf\\l'";
*/
  //draw the graph to stdout, which is this page :P
  $cmd= ("rrdtool graph - "
    ." -a PNG"                 //Output as an PNG Image
    ." --pango-markup"         //Render text with Pango
#    ." --border 1"            //Disable border
    ." -R light"               //Slight hinting and anti-aliasing
    ." -T 64"                  //Set tabstop width
    ." -n AXIS:8:Helvetica"
    ." -n UNIT:8:Helvetica"
    ." -n LEGEND:7:Helvetica"
    ." -c BACK#eeeeec00"     //Background colour
    ." -c CANVAS#eeeeec"     //Graph Background colour
    ." -c SHADEA#eeeeec00"   //Top and left shade
    ." -c SHADEB#eeeeec00"   //Bottom and right shade
    ." -c FONT#2e3436"       //Font colour
    ." -c AXIS#2e3436"       //Axis colour
    ." -c ARROW#2e3436"      //Axis arrow colour
    ." -c MGRID#babdb6"      //Major grid colour
    ." -c GRID#babdb6"       //Minor grid colour
    ." -c FRAME#2e3436"      //Frame colour
    ." -w $width"            //Width
    ." -h $height"           //Height
    ." -l 0"                 //Lower limit of graph
    ." $range"               //Time range
    ." -v '<b>Time to collect</b> Seconds'" //Left Vertical axis label
/*    ." --right-axis 10:0"     //Right Vertical axis
    ." --right-axis-label '<b>Nodes\tProbes</b>'" //Right Vertical axis label
    ." --right-axis-format '%.0lf'"*/
    ."$defs");

  $cmd .= " -E"; //Sloping edges

  //execute
  $xc = 0;
  system($cmd, $xc);
  if ($xc > 0) {
    echo "Graph Drawing Failed\n\n";
    echo $cmd;
  }
?>
