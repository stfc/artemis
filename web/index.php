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
  <body onload="setupJSON(); setInterval('updateProbesJSON()',30000); updateProbesJSON();"> 
    <div>
      <img src="images/logo-header.png" alt="ARTEMIS - Almost Real-Time Enviromental Monitoritoring &amp; Information System" />
    </div>
    <div id="themes">
      <p><a class="light" href=".">L</a> <a class="dark" href="?dark">D</a></p>
    </div>
    <div id="divRoom" style="width: 575px; height: 615px; background-image: url('rooms/room.png');"<?php //onmousemove="move(event);" onmouseup="drop();"?>></div>
<?php flush(); ?>
    <div id="divGraph">
      <form action="#" method="get">
        <p>
          <input name="date-start" id="inputDateStart" type="hidden"   value="<?php echo time()-604800; ?>" /><button type="button" id="btnCalendarStart">Start</button>
          <input name="date-end"   id="inputDateEnd"   type="hidden"   value="<?php echo time(); ?>"        /><button type="button" id="btnCalendarEnd">End</button>
          <button type="button" title="Shrink view" onclick="zoom_in();">&rarr; &larr;</button>
          <button type="button" title="Expand view" onclick="zoom_out();">&larr; &rarr;</button>
          <button type="button" title="Reset view"  onclick="zoom_reset();">Reset</button>
          <input name="baseline"   id="inputBaseline"  type="checkbox" title="In this mode, the first probe becomes the baseline and the other probes are normalised against it." onchange="updateGraph()">Baseline Mode</input>
        </p>
      </form>
      <script type="text/javascript">
        Calendar.setup({
          inputField     :    "inputDateStart",    // id of the input field
          ifFormat       :    "%s",                // format of the input field
          showsTime      :    true,                // will display a time selector
          button         :    "btnCalendarStart",  // trigger for the calendar (button ID)
          singleClick    :    false,               // double-click mode
          onUpdate       :    updateGraph,         //update graph dates
          step           :    1                    // show all years in drop-down boxes (instead of every other year as default)
        });
        Calendar.setup({
          inputField     :    "inputDateEnd",      // id of the input field
          ifFormat       :    "%s",                // format of the input field
          showsTime      :    true,                // will display a time selector
          button         :    "btnCalendarEnd",    // trigger for the calendar (button ID)
          singleClick    :    false,               // double-click mode
          onUpdate       :    updateGraph,         //update graph dates
          step           :    1                    // show all years in drop-down boxes (instead of every other year as default)
        });
      </script>
      <img id="imgGraph" src="" alt="Select probes to view" onmouseedown="zoom(event);" onmouseup="zoom(event);" onmousemove="zoom(event);"/>
    </div>
    <p>Click to compare up to six probe histories</p>
    <p id="update_time"><!--Filled by JavaScript--></p>
  </body>
</html>
