<!DOCTYPE html>
<?php

#
#  Copyright Science and Technology Facilities Council, 2009-2012.
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

function classOptions() {
  $classes = Array(
    "snmp_env_jacarta.node_jacarta",
    "snmp_env_swift.node_swiftCM1",
    "snmp_pdu_apc.node_apc_switched_pdu",
    "xml_env_swift.node_swiftCM1_xml",
  );
  
  foreach ($classes as $c) {
    echo "<option>$c</option>";
  }
}

function printConfig($config) {
  echo "<h2>Configuration</h2>\n";
  foreach ($config as $n => $s) {
    echo "<h3>$n</h3>\n";
    echo "<dl class='dl-horizontal'>\n";
    foreach($s as $k => $v) {
      if (is_array($v)) {
        $v = join(",", $v);
      }
      echo "<dt>$k</dt><dd>$v</dd>\n";
    }
    echo "</dl>\n";
  }
}


require("prepost.inc.php");

pre();

require_once("artemis_config.inc.php");

echo "<h1>{$config["room"]["name"]}</h1>\n";

if (isset($_GET["result"])) {
  echo "<p class=\"info\">Last update returned &quot;{$_GET["result"]}&quot;</p>\n";
}

$room_id = "ARTEMIS-STATS-".str_replace(" ", "_", $config["room"]["name"]);

echo "<h2>Performance</h2>\n";
echo "<a href=\"statsgraph.php?id=$room_id&amp;width=2400\">\n";
echo "<img src=\"statsgraph.php?id=$room_id\" alt=\"ARTEMIS System Statistics Graph\" />\n";
echo "</a>\n";

?>
<div class="container">
  <h2>Nodes</h2>
  <table class="table" border="1" id="tablenodes">
    <thead>
      <tr>
        <th>IP Address</th>
        <th>Module</th>
        <th>Class</th>
        <th>Last Contact</th>
      </tr>
    </thead>
    <tbody>
    </tbody>
  </table>
  <script type="text/javascript">
    $(document).ready(function() {
      $('#tablenodes').dataTable({
        "iDisplayLength" : 20,
        "aLengthMenu": [10, 20, 50, 100, 200, 500],
        "sAjaxSource": "api.php?list_nodes",
        "sPaginationType": "full_numbers",
      });
    } );
  </script>
</div>
<div class="container">
  <h2>Probes</h2>
  <table class="table" border="1" id="tableprobes">
    <thead>
      <tr>
        <th>ID</th>
        <th>Name</th>
        <th>x</th>
        <th>y</th>
        <th>z</th>
        <th>w</th>
        <th>h</th>
        <th>d</th>
        <th>Last Contact</th>
        <th>Remote Name</th>
      </tr>
    </thead>
    <tbody>
    </tbody>
  </table>
  <script type="text/javascript">
    $(document).ready(function() {
      $('#tableprobes').dataTable({
        "iDisplayLength" : 20,
        "aLengthMenu": [10, 20, 50, 100, 200, 500],
        "sAjaxSource": "api.php?list_probes",
        "sPaginationType": "full_numbers",
      });
    } );
  </script>
  <script type="text/javascript" charset="utf-8" src="http://ajax.aspnetcdn.com/ajax/jQuery/jquery-2.0.3.min.js"></script>
  <script type="text/javascript" charset="utf-8" src="http://ajax.aspnetcdn.com/ajax/jquery.dataTables/1.9.4/jquery.dataTables.min.js"></script>
</div>
<?php

printConfig($config);

?>
</body>
</html>
