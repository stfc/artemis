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

function pre() {
  echo <<<EOT
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
  <head>
    <link href="dropdown.css" rel="stylesheet" type="text/css" />
    <link href="main.css" rel="stylesheet" type="text/css" />
    <title>ARTEMIS</title>
    <meta http-equiv="Pragma" content="no-cache" />
    <meta http-equiv="Expires" content="-1" />
    <!-- ARTEMIS Specifics -->
    <link rel="icon" href="images/utilities-system-monitor.png" type="image/png" />
    <script type="text/javascript" src="sprintf.js"></script>
    <script type="text/javascript" src="functions.js"></script>
  </head>

EOT;

  flush();

  echo <<<EOT
  <body onload="setupJSON(); setInterval('updateProbesJSON()',30000); updateProbesJSON();" onresize="updateGraph();">
  <script type="text/javascript">

  function rollup(id) {
    if (document.getElementById(id).style.display == "none") {
      document.getElementById(id).style.display = "";
    } else {
      document.getElementById(id).style.display = "none";
    }
  }

  </script>

EOT;

  flush();

  return 0;
}


function post() {
  echo "  </body>\n";
  echo "</html>\n";

  flush();

  return 0;
}
?>
