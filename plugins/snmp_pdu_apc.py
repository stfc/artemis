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
# APC Switched Rack PDU, e.g. AP7953
#  Good example of a simpler, single probe node
#
class node(node):
    def __init__(self, ip, community='public'):
        self.ip        = ip
        self.community = community
    def fetch(self):
        #unit id
        model  = getMIB(self.ip, ".1.3.6.1.4.1.318.1.1.12.1.5.0", self.community)
        if model is None:
            #Can't find a valid sensor, so abort
            return []
        else:
            model = model[0]

        serial = getMIB(self.ip, ".1.3.6.1.4.1.318.1.1.12.1.6.0", self.community)
        if serial is None:
            #Can't find a valid sensor, so abort
            return []
        else:
            serial = serial[0]

        id = "CURRENT-" + model + "-" + serial

        #Get value or on-board current monitor
        if model == "AP7921":
            #Just get the single current value
            value = getMIB(self.ip, ".1.3.6.1.4.1.318.1.1.12.2.3.1.1.2", self.community)
            if value is None:
                return []
            else:
                value = value[0]

        elif model == "AP7953":
            #This model has three current monitors, Bank 1, Bank 2 and Total, we only want the total current
            value = getMIB(self.ip, ".1.3.6.1.4.1.318.1.1.12.2.3.1.1.2.3", self.community)
            if value is None:
                return []
            else:
                value = value[0]

        else:
            return []

        #Scale value, PDU returns Amps*10
        value = float(value) / 10

        #Units of measurement
        unit = UNIT_CURRENT

        return [(id, value, unit, "")]
