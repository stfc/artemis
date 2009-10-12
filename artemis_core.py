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
from threading import Thread

SNMP_TIMEOUT = 5 #Timeout of snmp requests in seconds
SNMP_RETRIES = 2 #Number of snmp request retries

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

#Misc functions
def getMIB(ip, mib, community = "public"):
  (x, d) = commands.getstatusoutput("/usr/bin/snmpwalk -r " + str(SNMP_RETRIES) + " -t " + str(SNMP_TIMEOUT) + " -v 1 -c " + community + " -O v " + ip + " " + mib + " | grep -v 'End of MIB'")
  if (x == 0):
    d = d.splitlines()
    d = [r.split(': ')[-1].replace('"', '').replace(' ', '_') for r in d]
    return d
  else:
    return None

#Data fetch loop
def grabData(nodeset):
  dataset = []
  grabbers = []

  for node in nodeset:
    current = data_grabber(node)
    grabbers.append(current)
    current.start()

  for grabber in grabbers:
    grabber.join()
    dataset += grabber.data
    
  return dataset

#Thread object for grabbing data from nodes
class data_grabber(Thread):
  #Sets up thread, ready to go
  def __init__(self, node):
    Thread.__init__(self)
    self.node = node
    self.data = None
  #Called by start(), does the actual data collection
  def run(self):
    data = self.node.fetch()
    if (data != None):
      self.data = data

#Import all defined datasource nodes
from artemis_node_snmp_jacarta import *
from artemis_node_snmp_swift   import *
from artemis_node_xml_swift    import *
from artemis_node_snmp_pdu_apc import *

