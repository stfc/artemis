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

require_once("artemis_config.inc.php");

$PAGES = Array(
  "." => "Display",
  "admin.php" => "Admin",
);

function pre() {
  global $PAGES;
  echo <<<EOT
<!DOCTYPE html>
<html>
  <head>
    <link href="dropdown.css" rel="stylesheet" type="text/css">
    <title>ARTEMIS</title>
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="-1">
    <!-- ARTEMIS Specifics -->
    <link rel="icon" href="images/utilities-system-monitor.png" type="image/png">
    <link href="http://netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css" rel="stylesheet" type="text/css">
    <link href="http://ajax.aspnetcdn.com/ajax/jquery.dataTables/1.9.4/css/jquery.dataTables.css" type="text/css">
    <link href="css/bootstrap-datetimepicker.min.css" rel="stylesheet" type="text/css">
    <link href="css/main.css" rel="stylesheet" type="text/css">
    <script type="text/javascript" src="http://code.jquery.com/jquery-2.0.3.min.js"></script>
    <script type="text/javascript" src="http://netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min.js"></script>
    <script type="text/javascript" src="js/sprintf.js"></script>
    <script type="text/javascript" src="js/moment.js"></script>
    <script type="text/javascript" src="js/functions.js"></script>
  </head>
  <body>
    <nav class="navbar navbar-default navbar-inverse navbar-static-top" role="navigation">
      <div class="navbar-header">
        <a class="navbar-brand" href="./"><img src="images/logo-header.png" alt="ARTEMIS - Almost Real-Time Enviromental Monitoritoring &amp; Information System"></a>
      </div>
      <div class="collapse navbar-collapse navbar-ex1-collapse">
        <ul class="nav navbar-nav">

EOT;

  $page = parse_url($_SERVER["REQUEST_URI"], PHP_URL_PATH);

  if (substr($page, -1) == "/") {
    $page = ".";
  }
  echo "<!-- page = " . $page . " -->\n";

  foreach ($PAGES as $url => $name) {
     echo "<li";
     if (preg_match("/".preg_quote($url)."\$/", $page) > 0) {
       echo " class='active'";
     }
     echo"><a href='$url'><br>$name</a></li>\n";
  }

  echo <<<EOT
        </ul>
      </div>
    </nav>

EOT;

  flush();

  echo <<<EOT
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
  </body>
  </html>
EOT;

  flush();

  return 0;
}
?>
