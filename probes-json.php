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

  header('Content-type: application/json');
  header('Content-Disposition: attachment; filename="probes.json"');

  //open the csv file
  $file_handle = fopen("data/probe-data.csv", "r") or exit;

  //create an empty array
  $a_probes = Array();

  //iterate through the csv file constructing an array of probe data
  $i = 1;
  while (!feof($file_handle) ) {
    $line = fgetcsv($file_handle, 1024);
    if ($line != null) {
                              //  ProbeID   Value            Tile X    Tile Y    Size X    Size Y
      array_push($a_probes, array($line[0], round($line[1]), $line[3], $line[4], $line[5], $line[6])); #The value is rounded to save space, which is not ideal, but a good compromise
      $i++;
    }
  }

  //close the csv file
  fclose($file_handle);

  //encode the array as text with JSON
  echo json_encode($a_probes);
?>
