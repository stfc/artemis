#!/usr/bin/python
# coding=utf8

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

from base import *

##
# Jacarta network attached monitoring unit
#
class node(node):
    def fetch(self):
        #temperature probes
        i = getMIB(self.ip, ".1.3.6.1.4.1.3854.1.2.2.1.16.1.1")
        if (i is not None):
            ids_temp = i
        else:
            ids_temp = []

        v = getMIB(self.ip, ".1.3.6.1.4.1.3854.1.2.2.1.16.1.3")
        if (v is not None):
            values_temp = v
        else:
            values_temp = []

        #build list of units
        units_temp = []
        for i in ids_temp:
            units_temp += [UNIT_TEMPERATURE]

        #humidity sensors
        i = getMIB(self.ip, ".1.3.6.1.4.1.3854.1.2.2.1.17.1.1")
        if (i is not None):
            ids_humid = i

        v = getMIB(self.ip, ".1.3.6.1.4.1.3854.1.2.2.1.17.1.3")
        if (v is not None):
            values_humid = v

        #cast all values as integers
        values_humid = [int(v) for v in values_humid]

        #build list of units
        units_humid = []
        for i in ids_humid:
            units_humid += [UNIT_HUMIDITY]

        #Concatenate data sets
        ids    = ids_temp    + ids_humid
        values = values_temp + values_humid
        units  = units_temp  + units_humid

        names = ["" for v in values]

        return zip(ids, values, units)
