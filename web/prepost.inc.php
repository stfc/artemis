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
<!DOCTYPE html>
<html>
  <head>
    <link href="dropdown.css" rel="stylesheet" type="text/css" />
    <link href="main.css" rel="stylesheet" type="text/css" />
    <title>ARTEMIS</title>
    <meta http-equiv="Pragma" content="no-cache" />
    <meta http-equiv="Expires" content="-1" />
    <!-- ARTEMIS Specifics -->
    <link rel="icon" href="images/utilities-system-monitor.png" type="image/png" />
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.5/jquery.min.js"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/jquery-ui.min.js"></script>
    <script type="text/javascript" src="sprintf.js"></script>
    <script type="text/javascript" src="moment.js"></script>
    <script type="text/javascript" src="functions.js"></script>
  </head>

EOT;

  flush();

  echo <<<EOT
  <body onresize="updateGraph();">
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
  echo <<<EOT
    <div id="footer">
      <a href="http://www.w3.org/html/logo/"><img src="images/HTML5_Badge_32.png" width="32" height="32" alt="HTML5 Powered" title="HTML5 Powered"></a>
    </div>
  </body>
  </html>
EOT;

  flush();

  return 0;
}
?>
