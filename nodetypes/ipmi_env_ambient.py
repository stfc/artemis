#!/usr/bin/python
# coding=utf8

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

from base import *

import re

##
# 1-Wire network attached monitoring base
#  Good example of a complex, multi probe node
#
class node_ipmiAmb(node):
    def __init__(self, ip, user = "ADMIN", password = "ADMIN"):
        self.ip = ip
        self.user = user
        self.password = password
        self.reMac = re.compile("([0-9A-F][0-9A-F]:[0-9A-F][0-9A-F]:[0-9A-F][0-9A-F]:[0-9A-F][0-9A-F]:[0-9A-F][0-9A-F]:[0-9A-F][0-9A-F])")
        self.reSens = re.compile("([0-9]+): ([A-Za-z0-9 ]+) \(([A-Za-z]+)\): ([0-9]+.[0-9]+) C \((NA|[0-9]+.[0-9]+)/(NA|[0-9]+.[0-9]+)\): \[([A-Z]+)\]")


    def fetch(self):
        results = []

        (x, d) = commands.getstatusoutput("/usr/sbin/bmc-config -h %s -u %s -p %s --checkout -e Lan_Conf:MAC_Address" % (self.ip, self.user, self.password))
        if (x == 0):
            mac = self.reMac.search(d)
            if mac:
                mac = mac.groups()[0]
                (x, d) = commands.getstatusoutput("/usr/sbin/ipmi-sensors -g Temperature -h %s -u %s -p %s" % (self.ip, self.user, self.password))
                if (x == 0):
                    d = d.splitlines()
                    for l in d:
                        sensor = self.reSens.match(l)
                        if sensor:
                            (id, name, type, value, lower, upper, status)  = sensor.groups()
                            if type == "Temperature" and ("Amb" in name or "Sys" in name) and value != "0.00":
                                value = float(value)
                                id = "%s-IPMI-%s-%s" % (type.upper(), mac.replace(":", ""), id)
                                results.append((id, value, "C", name))

        return results
