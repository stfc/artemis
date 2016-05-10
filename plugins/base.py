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

import commands

#Units
UNIT_TEMPERATURE = "C"
UNIT_CURRENT     = "A"
UNIT_AIRFLOW     = "%"
UNIT_HUMIDITY    = "%"

#Translation tables for ID codes and units
FAMILY_1WIRE = {
    "28": ("TEMPERATURE", UNIT_TEMPERATURE),
    "14": ("AIRFLOW",     UNIT_AIRFLOW)
}

#SNMP Settings
SNMP_TIMEOUT = 8 #Timeout of snmp requests in seconds
SNMP_RETRIES = 2 #Number of snmp request retries

def getMIB(ip, mib, community = "public"):
    """ Fetch contents of a mib by walking the tree from a defined point"""
    (x, d) = commands.getstatusoutput(
        "/usr/bin/snmpwalk -r %s -t %s -v 1 -c %s -O v %s %s | grep -v 'End of MIB'" % (
            SNMP_RETRIES,
            SNMP_TIMEOUT,
            community,
            ip,
            mib
        )
    )
    if (x == 0):
        d = d.splitlines()
        d = [r.split(': ')[-1].replace('"', '').replace(' ', '_') for r in d]
        return d
    else:
        print("  ERROR: getMIB on " + ip + " non-zero exit code")
        return None

class node(object):
    def __init__(self, ip, username="", password=""):
        self.ip = ip
        self.username = username
        self.password = password
    def fetch(self):
        pass
