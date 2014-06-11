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
  <div id="controls">
    <form onchange="updateProbesJSON();">
      <label><input class="checkbox-inline" type="checkbox" name="temperature" id="inputTemperature" checked="checked"> Temperature</label>
      <label><input class="checkbox-inline" type="checkbox" name="humidity"    id="inputHumidity"> Humidity</label>
      <label><input class="checkbox-inline" type="checkbox" name="airflow"     id="inputAirflow"> Airflow</label>
      <label><input class="checkbox-inline" type="checkbox" name="current"     id="inputCurrent"> Current</label>
    </form>
  </div>
<?php
  $w = $config['room']['width'];
  $h = $config['room']['height'];

  if (!isset($_REQUEST['nobg'])) {
    $s = " background-image: url('images/room.png');";
  }
?>
<?php flush(); ?>
  <div class="row">
    <div id="divRoom" class="col-md-4" style="width: <?php echo $w ?>px; height: <?php echo $h ?>px;<?php echo $s ?>">
    </div>
    <div id="divGraph" class="col-md-8">
      <div>
        <form role="form" class="form-inline">
          <div>
            <div class="form-group">
              <label>Start:</label>
              <div class='input-group date' id='datetimepickerStart' data-date-format="hh:mm DD.MM.YYYY">
                <input class="form-control" type="text" id="inputDateStart" value="<?php echo Date("H:i d.m.Y", time()-604800); ?>" onchange="updateGraph()">
                <span class="input-group-addon"><span class="fa fa-calendar"></span></span>
              </div>
            </div>
            <div class="form-group">
              <label>End:</label>
              <div class='input-group date' id='datetimepickerEnd' data-date-format="hh:mm DD.MM.YYYY">
                <input class="form-control" type="text" id="inputDateEnd" value="<?php echo Date("H:i d.m.Y"); ?>" onchange="updateGraph()">
                <span class="input-group-addon"><span class="fa fa-calendar"></span></span>
              </div>
            </div>
          </div>
          <div>
            <div class="form-group">
              <label>
                <input class="checkbox-inline" type="checkbox" name="baseline" id="inputBaseline" title="Use first probe as baseline and normalise other probes against it." onchange="updateGraph()"> Baseline Mode
              </label>
            </div>
            <div class="form-group">
              <label>
                <input class="checkbox-inline" type="checkbox" name="trend" id="inputTrend" title="Automatically smooth noisy data to a trendline." onchange="updateGraph()"> Auto Trend
              </label>
            </div>
          </div>
        </form>
      </div>
      <div id="minfo">&nbsp;</div>
      <div>
        <img id="imgGraph" src="drawgraph.php" alt="Select probes to view">
      </div>
    </div>
  </div>
  <script type="text/javascript" src="js/bootstrap-datetimepicker.min.js"></script>
  <script type="text/javascript">
    function update() {
      $.getJSON("data/data-dump.json", callbackJSON);
    }

    $(function() {
      setInterval('update()',30000);
      update();

      $('#datetimepickerStart').datetimepicker({
        pickSeconds: false,
        icons: {
          time: "fa fa-clock-o",
          date: "fa fa-calendar",
          up: "fa fa-arrow-up",
          down: "fa fa-arrow-down"
        }
      });
      $('#datetimepickerStart').on('changeDate', function(e) {
        updateGraph();
      });

      $('#datetimepickerEnd').datetimepicker({
        pickSeconds: false,
        icons: {
          time: "fa fa-clock-o",
          date: "fa fa-calendar",
          up: "fa fa-arrow-up",
          down: "fa fa-arrow-down"
        }
      });
      $('#datetimepickerEnd').on('changeDate', function(e) {
        updateGraph();
      });
    });

    $(window).resize(updateGraph);

    var graph_embiggened = false;

    $("#imgGraph").click(function() {
      graph_embiggened = ! graph_embiggened;
      updateGraph();
    });

    var minfo_vis = false;

    $("#imgGraph").mousemove(function(e) {
      if (meta != null) {
        var parentOffset = $(this).offset();
        $("#minfo").offset({
          left: e.pageX + 8,
          top: e.pageY + 8
        });
        var x = e.pageX - parentOffset.left - meta["graph_left"];
        var y = meta["graph_height"] - (e.pageY - parentOffset.top - meta["graph_top"]);

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
<?php
  post();
?>
