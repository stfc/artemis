#!/usr/bin/python

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

import commands, subprocess, urllib

#Units
UNIT_TEMPERATURE = chr(176) + "C"
UNIT_CURRENT     = "A"
UNIT_AIRFLOW     = "%"
UNIT_HUMIDITY    = "%"

#Translation tables for ID codes and units
FAMILY_1WIRE = {
  "28": ("TEMPERATURE", UNIT_TEMPERATURE),
  "14": ("AIRFLOW",     UNIT_AIRFLOW)
}

#SNMP Settings
SNMP_TIMEOUT = 5 #Timeout of snmp requests in seconds
SNMP_RETRIES = 2 #Number of snmp request retries

def getMIB(ip, mib, community = "public"):
  """ Fetch contents of a mib by walking the tree from a defined point"""
  (x, d) = commands.getstatusoutput("/usr/bin/snmpwalk -r " + str(SNMP_RETRIES) + " -t " + str(SNMP_TIMEOUT) + " -v 1 -c " + community + " -O v " + ip + " " + mib + " | grep -v 'End of MIB'")
  if (x == 0):
    d = d.splitlines()
    d = [r.split(': ')[-1].replace('"', '').replace(' ', '_') for r in d]
    return d
  else:
    return None

class node(object):
  def __init__(self, ip):
    self.ip        = ip
  def fetch(self):
    pass
