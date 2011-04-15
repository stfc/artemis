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
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
  <head>
    <link href="main.css" rel="stylesheet" type="text/css" />
<?php
  if (isset($_REQUEST['dark'])) {
    echo '    <link href="dark.css" rel="stylesheet" type="text/css" />';
  }
?>
    <title>ARTEMIS</title>
    <meta http-equiv="Pragma" content="no-cache" />
    <meta http-equiv="Expires" content="-1" />
    <!-- ARTEMIS Specifics -->
    <link rel="icon" href="images/utilities-system-monitor.png" type="image/png" />
    <script type="text/javascript" src="sprintf.js"></script>
    <script type="text/javascript" src="functions.js"></script>
    <!-- For jsCalendar -->
    <link rel="stylesheet" type="text/css" media="all" href="jscalendar/calendar-stfc-ral.css" />
    <script type="text/javascript" src="jscalendar/calendar.js"></script>
    <script type="text/javascript" src="jscalendar/lang/calendar-en.js"></script>
    <script type="text/javascript" src="jscalendar/calendar-setup.js"></script>
  </head>
<?php flush(); ?>
  <body onload="setupJSON(); setInterval('updateProbesJSON()',30000); updateProbesJSON();" onresize="updateGraph();"> 
    <div id="header">
      <img src="images/logo-header.png" alt="ARTEMIS - Almost Real-Time Enviromental Monitoritoring &amp; Information System" />
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
  echo "    <div id=\"divRoom\" style=\"width: ${w}px; height: ${h}px; background-image: url('rooms/room.png');\"></div>";
?>
<?php flush(); ?>
    <div id="divGraph">
      <form action="#" method="get">
        <p>
          <button type="button"    title="Set Start Date" id="btnCalendarStart">Start</button>
          <button type="button"    title="Set End Date"   id="btnCalendarEnd">End</button>
          <button type="button"    title="Shrink view"    onclick="zoom_in();">&rarr; &larr;</button>
          <button type="button"    title="Expand view"    onclick="zoom_out();">&larr; &rarr;</button>
          <button type="button"    title="Move Backwards" onclick="zoom_back();">&larr;</button>
          <button type="button"    title="Move Forwards"  onclick="zoom_forward();">&rarr;</button>
          <button type="button"    title="Reset view"     onclick="zoom_reset();">Reset</button>
        </p>
        <p>
          <input  type="checkbox"  name="baseline"        id="inputBaseline"  title="Use first probe as baseline and normalise other probes against it." onchange="updateGraph()">Baseline Mode</input>
          <input  type="checkbox"  name="trend"           id="inputTrend"     title="Automatically smooth noisy data to a trendline." onchange="updateGraph()">Auto Trend</input>
          <input  type="hidden"    name="date-start"      id="inputDateStart" value="<?php echo time()-604800; ?>" />
          <input  type="hidden"    name="date-end"        id="inputDateEnd"   value="<?php echo time(); ?>"        />
        </p>
      </form>
      <script type="text/javascript">
        Calendar.setup({
          inputField     :    "inputDateStart",    // id of the input field
          ifFormat       :    "%s",                // format of the input field
          showsTime      :    true,                // will display a time selector
          button         :    "btnCalendarStart",  // trigger for the calendar (button ID)
          singleClick    :    false,               // double-click mode
          onUpdate       :    updateGraph,         // update graph dates
          showOthers     :    true,                // show days belonging to other months
          cache          :    true,                // use one object for all calendars
          step           :    1                    // show all years in drop-down boxes (instead of every other year as default)
        });
        Calendar.setup({
          inputField     :    "inputDateEnd",      // id of the input field
          ifFormat       :    "%s",                // format of the input field
          showsTime      :    true,                // will display a time selector
          button         :    "btnCalendarEnd",    // trigger for the calendar (button ID)
          singleClick    :    false,               // double-click mode
          onUpdate       :    updateGraph,         // update graph dates
          showOthers     :    true,                // show days belonging to other months
          cache          :    true,                // use one object for all calendars
          step           :    1                    // show all years in drop-down boxes (instead of every other year as default)
        });
      </script>
      <img id="imgGraph" src="" alt="Select probes to view" onmouseedown="zoom(event);" onmouseup="zoom(event);" onmousemove="zoom(event);"/>
    </div>
  </body>
</html>
