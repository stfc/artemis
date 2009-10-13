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

  function scaleColour($temp)
  {
    $t = $temp;
    #range of temperature scale
    $t_min = 10;
    $t_max = 50;

    #range of colour scale
    $c_min = 0;
    $c_max = 255;

    #Clip the temperature to the above range
    $t = max($t_min, $t);
    $t = min($t_max, $t);

    #Apply transformation
    $result = ((($t - $t_min) / ($t_max - $t_min)) * ($c_max - $c_min)) + $c_min;

    $r = $result;
    $g = 0;
    $b = 255 - $result;

    $colour = sprintf('%02X%02X%02X', $r, $g, $b);

    return $colour;
  }

?>
