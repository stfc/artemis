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
            <input  type="checkbox"  name="bms"             id="inputBms"       title="Show BMS events on graph." onchange="updateGraph()">BMS Events</input>
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
        <img id="imgGraph" src="" alt="Select probes to view" />
      </div>
    </div>
<?php

post();

?>
