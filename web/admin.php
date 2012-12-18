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
    echo "<dl>\n";
    foreach($s as $k => $v) {
      if (is_array($v)) {
        $v = join(",", $v);
      }
      echo "<dt>$k</dt><dd>$v</dd>\n";
    }
    echo "</dl>\n";
  }
}


?>
<html>
<head>
<link href="main.css" rel="stylesheet" type="text/css" />
</head>
<body>
<div id="header">
<img src="images/logo-header.png" alt="ARTEMIS - Almost Real-Time Enviromental Monitoritoring &amp; Information System" />
</div>
<link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/themes/base/jquery-ui.css" rel="stylesheet" type="text/css"/>
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.5/jquery.min.js"></script>
<script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/jquery-ui.min.js"></script>
<script type="text/javascript">

function addNode() {
  $("#dialogAddNode").dialog({
/*    buttons: [
      {
        text: "Ok",
        click: function() { $(this).dialog("close"); }
      }
  ],*/
    minWidth: 400,
    resizable: false,
    draggable: false,
    modal: true,
  });
}

function removeNode(ip) {
  if (confirm("Really remove probe " + ip + "?")) {
    window.location = "api.php?return=setup.php&action=removenode&ip="+ip;
  }
}

function removeProbe(p) {
  confirm("Really remove probe " + p + "?");
}

</script>
<div id="dialogAddNode" title="Add Node" style="display: none">
  <form id="formAddNode" action="api.php">
    <input type="hidden" name="action" value="addnode"></input>
    <input type="hidden" name="return" value="setup.php"></input>
    <div>
      <label for="inputIP">IP Address<label>
      <input id="inputIP" name="ip"></input>
    </div>
    <div>
      <label for="selectClass">Class</label>
      <select id="selectClass" name="class"><?php classOptions(); ?></select>
    </div>
    <div>
      <button action="submit">Add</button>
    </div>
  </form>
</div>

<div id="floater">
  <p><a href=".">Main Display</a></p>
</div>

<?php

require_once("artemis_config.inc.php");

echo "<h1>{$config["room"]["name"]}</h1>\n";

if (isset($_GET["result"])) {
  echo "<p class=\"info\">Last update returned &quot;{$_GET["result"]}&quot;</p>\n";
}

$room_id = "ARTEMIS-STATS-".str_replace(" ", "_", $config["room"]["name"]);

echo "<h2>Performance</h2>\n";
echo "<a href=\"statsgraph.php?id=$room_id&width=2400\">\n";
echo "<img src=\"statsgraph.php?id=$room_id\" />\n";
echo "</a>\n";

echo "</ul>\n";

$db = new PDO($config["store"]["driver"].':../'.$config["store"]["path"]);

if ($db) {

  echo "<h2>Nodes</h2>\n";
  $nodes = $db->query('SELECT * FROM nodes order by ip');
  if ($nodes) {
    echo "<table>\n";
    echo "<tr><th>IP Address</th><th>Module</th><th>Object Class</th><th>Last Contact</th><th>&nbsp;</th></tr>\n";
    foreach($nodes as $n) {
      echo "<tr><td>{$n["ip"]}</td><td>{$n["module"]}</td><td>{$n["object"]}</td><td>{$n["lastcontact"]}</td><td><img src=\"/icons/actions/list-remove.png\" onclick=\"removeNode('{$n["ip"]}')\" /></td></tr>\n";
    }
    echo "</table>\n";
    echo "<p><a href=\"javascript:addNode()\"><img src=\"/icons/actions/list-add.png\" />Add Node</a></p>\n";
  }

  echo "<h2>Probes</h2>\n";
  $probes = $db->query('SELECT * FROM probes order by lastcontact desc');
  if ($probes) {
    echo "<table>\n";
    echo "<tr><th>ID</th><th>Name</th><th>x</th><th>y</th><th>z</th><th>w</th><th>h</th><th>d</th><th>Last Contact</th><th>Remote Name</th><th>&nbsp;</th></tr>\n";
    foreach($probes as $p) {
      echo "<tr>";
      echo "<td>{$p["id"]}</td>";
      echo "<td>{$p["name"]}</td>";
      echo "<td>".sprintf("%2.2f", $p["x"])."</td>";
      echo "<td>".sprintf("%2.2f", $p["y"])."</td>";
      echo "<td>".sprintf("%2.2f", $p["z"])."</td>";
      echo "<td>".sprintf("%2.2f", $p["w"])."</td>";
      echo "<td>".sprintf("%2.2f", $p["h"])."</td>";
      echo "<td>".sprintf("%2.2f", $p["d"])."</td>";
      $lastcontact = (time() - strtotime($p["lastcontact"]));
      echo "<td>";
      if ($p["lastcontact"]) {
        if ($lastcontact > 60) {
          echo $lastcontact." seconds ago";
        } else {
          echo "Last Run";
        }
      } else {
        echo "Never";
      }
      echo "</td>";
      echo "<td>".($p["remote_name"])."</td>";
      echo "<td>";
      echo "<img src=\"/icons/actions/document-properties.png\" onclick=\"editProbe('{$p["id"]}')\"/>";
      if ($lastcontact > 60) {
        echo "&nbsp;<img src=\"/icons/actions/list-remove.png\" onclick=\"removeProbe('{$p["id"]}')\" />";
      }
      echo "</td>";
      echo "</tr>\n";
    }
    echo "</table>\n";
  }

}

printConfig($config);

?>
</body>
</html>
