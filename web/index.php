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
#  $Revision: 9148 $
#  $Date: 2011-09-28 14:22:35 +0100 (Wed, 28 Sep 2011) $
#  $LastChangedBy: tkk76468@FED.CCLRC.AC.UK $
#
?>
<!DOCTYPE html>
<html>
  <head>
    <link href="main.css" rel="stylesheet" type="text/css" />
<?php

  require("prepost.inc.php");

  pre();

?>
  <div id="header">
    <img src="images/logo-header.png" alt="ARTEMIS - Almost Real-Time Enviromental Monitoritoring &amp; Information System" />
  </div>
  <div id="floater">
    <p><a href="admin.php">Admin</a></p>
  </div>
  <div id="controls">
    <form action="#" method="get" onchange="updateProbesJSON();">
      <input type="checkbox" name="temperature" id="inputTemperature" checked="checked">Temperature</input>
      <input type="checkbox" name="humidity"    id="inputHumidity">Humidity</input>
      <input type="checkbox" name="airflow"     id="inputAirflow">Airflow</input>
      <input type="checkbox" name="current"     id="inputCurrent">Current</input>
    </form>
  </div>
<?php
  //Get size of room from image
  $s = getimagesize('rooms/room.png');
  $w = $s[0];
  $h = $s[1];
  $s = " background-image: url('rooms/room.png');";
  if (isset($_REQUEST['nobg'])) {
    $s = "";
  }

  echo "    <div id=\"divRoom\" style=\"width: ${w}px; height: ${h}px; $s\"></div>";
?>
<?php flush(); ?>
    <div id="divGraph">
      <form action="#" method="get">
        <p>
          Start: <input type="text" size="8" name="date-start" id="inputDateStart" value="<?php echo Date("Y-m-d", time()-604800); ?>" />
          End: <input type="text" size="8" name="date-end"   id="inputDateEnd"   value="<?php echo Date("Y-m-d"); ?>" />
          <!--<button type="button"    title="Shrink view"    onclick="zoom_in();">&rarr; &larr;</button>
          <button type="button"    title="Expand view"    onclick="zoom_out();">&larr; &rarr;</button>
          <button type="button"    title="Move Backwards" onclick="zoom_back();">&larr;</button>
          <button type="button"    title="Move Forwards"  onclick="zoom_forward();">&rarr;</button>
          <button type="button"    title="Reset view"     onclick="zoom_reset();">Reset</button>-->
        </p>
        <p>
          <input  type="checkbox"  name="baseline"        id="inputBaseline"  title="Use first probe as baseline and normalise other probes against it." onchange="updateGraph()" />Baseline Mode
          <input  type="checkbox"  name="trend"           id="inputTrend"     title="Automatically smooth noisy data to a trendline." onchange="updateGraph()" />Auto Trend
          <input  type="checkbox"  name="bms"             id="inputBms"       title="Show BMS events on graph." onchange="updateGraph()" />BMS Events
        </p>
      </form>
      <div id="minfo">&nbsp;</div>
      <img id="imgGraph" src="drawgraph.php" alt="Select probes to view" />
      <script type="text/javascript">
        function update() {
          $.getJSON("data/data-dump.json", callbackJSON);
        }
        setInterval('update()',30000);
        update();

        $( "#inputDateStart" ).change(updateGraph);
        $( "#inputDateStart" ).datepicker({
          dateFormat : "yy-mm-dd",
        });
        
        $( "#inputDateEnd" ).change(updateGraph);
        $( "#inputDateEnd" ).datepicker({
          dateFormat : "yy-mm-dd",
        });

        $("#imgGraph").click(function(stuff) {
          if (ids.length > 0) {
            $u = stuff.target.src;
            $u = $u.replace(/width=[0-9]+/g, "width=" + window.innerWidth);
            $u = $u.replace(/height=[0-9]+/g, "height=" + window.innerHeight);
            window.location = $u;
          }
        });

        var minfo_vis = false;

        $("#imgGraph").mousemove(function(e) {
          if (meta != null) {
            var x = e.pageX - this.offsetLeft - meta["graph_left"];
            var y = meta["graph_height"] - (e.pageY - this.offsetTop - meta["graph_top"]);
            if (x >= 0 && y >= 0 && x <= meta["graph_width"] && y <= meta["graph_height"]) {

              x = meta["graph_start"] + ((x / meta["graph_width"]) * (meta["graph_end"] - meta["graph_start"]));
              x = moment.unix(x).format('YYYY-MM-DD HH:mm') 

              y = meta["value_min"]   + ((y / meta["graph_height"]) * meta["value_max"]);
              y = y.toFixed(1);

              $("#minfo").html(x + "<br />" + y + "C");
              if (! minfo_vis) {
                $("#minfo").show();
                minfo_vis = true;
              }
              $("#imgGraph").css("cursor", "crosshair");
            }
            else {
              if (minfo_vis) {
                $("#minfo").hide();
                minfo_vis = false;
              }
              $("#imgGraph").css("cursor", "");
            }
          }
        });
      </script>
    </div>
<?php
  post();
?>
