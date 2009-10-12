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
from xml.dom import minidom
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

#Main Classes
class node(object):
  def __init__(self, ip):
    self.ip        = ip
  def fetch(self):
    pass

##
# 1-Wire network attached monitoring base
#  Good example of a complex, multi probe node
#
class node_swiftCM1(node):
  def fetch(self):
    #temperature probes
    i = getMIB(self.ip, ".1.3.6.1.4.1.17373.2.4.1.2")
    if (i != None):
      ids = i
    else:
      ids = []

    v = getMIB(self.ip, ".1.3.6.1.4.1.17373.2.4.1.5")
    if (v != None):
      values = v
    else:
      values = []

    #airflow sensors
    i = getMIB(self.ip, ".1.3.6.1.4.1.17373.2.5.1.2")
    if (i != None):
      ids += i

    v = getMIB(self.ip, ".1.3.6.1.4.1.17373.2.5.1.5")
    if (v != None):
      values += v

    units = [FAMILY_1WIRE[i[-2:]][1] for i in ids]

    #This may look confusing, it's just splitting the ID up into parts
    ids   = [FAMILY_1WIRE[i[-2:]][0] + "-1WIRE-" + i[2:-2] + i[:2] for i in ids]
    
    values = [int(v) for v in values]

    return zip(ids, values, units)

##
# 1-Wire Network attached monitoring base, using XML interface instead of SNMP
#
class node_swiftCM1_xml(node):
  def fetch(self):
    #Fetch data
    data = urllib.urlopen('http://' + self.ip + '/data.xml')
    data = minidom.parse(data)

    return data

    #temperature probes
    if (i != None):
      ids = i
    else:
      ids = []

    v = getMIB(self.ip, ".1.3.6.1.4.1.17373.2.4.1.5")
    if (v != None):
      values = v
    else:
      values = []

    #airflow sensors
    i = getMIB(self.ip, ".1.3.6.1.4.1.17373.2.5.1.2")
    if (i != None):
      ids += i

    v = getMIB(self.ip, ".1.3.6.1.4.1.17373.2.5.1.5")
    if (v != None):
      values += v

    units = [FAMILY_1WIRE[i[-2:]][1] for i in ids]

    #This may look confusing, it's just splitting the ID up into parts
    ids   = [FAMILY_1WIRE[i[-2:]][0] + "-1WIRE-" + i[2:-2] + i[:2] for i in ids]
    
    values = [int(v) for v in values]

    return zip(ids, values, units)

##
# APC Switched Rack PDU, e.g. AP7953
#  Good example of a simpler, single probe node
#
class node_apc_switched_pdu(node):
  def __init__(self, ip, community='public'):
    self.ip        = ip
    self.community = community
  def fetch(self):
    #unit id
    model  = getMIB(self.ip, ".1.3.6.1.4.1.318.1.1.12.1.5.0", self.community)
    if model == None:
      #Can't find a valid sensor, so abort
      return []
    else:
      model = model[0]

    serial = getMIB(self.ip, ".1.3.6.1.4.1.318.1.1.12.1.6.0", self.community)
    if serial == None:
      #Can't find a valid sensor, so abort
      return []
    else:
      serial = serial[0]

    id = "CURRENT-" + model + "-" + serial

    #Get value or on-board current monitor
    if model == "AP7921":
      #Just get the single current value
      value = getMIB(self.ip, ".1.3.6.1.4.1.318.1.1.12.2.3.1.1.2", self.community)
      if value == None:
        return []
      else:
        value = value[0]

    elif model == "AP7953":
      #This model has three current monitors, Bank 1, Bank 2 and Total, we only want the total current
      value = getMIB(self.ip, ".1.3.6.1.4.1.318.1.1.12.2.3.1.1.2.3", self.community)
      if value == None:
        return []
      else:
        value = value[0]

    else:
      return []

    #Scale value, PDU returns Amps*10
    value = float(value) / 10

    #Units of measurement
    unit = UNIT_CURRENT
    
    return [(id, value, unit)]


##
# Jacarta network attached monitoring unit
#
class node_jacarta(node):
  def fetch(self):
    #temperature probes
    i = getMIB(self.ip, ".1.3.6.1.4.1.3854.1.2.2.1.16.1.1")
    if (i != None):
      ids_temp = i
    else:
      ids_temp = []

    v = getMIB(self.ip, ".1.3.6.1.4.1.3854.1.2.2.1.16.1.3")
    if (v != None):
      values_temp = v
    else:
      values_temp = []

    #build list of units
    units_temp = []
    for i in ids_temp:
      units_temp += [UNIT_TEMPERATURE]

    #humidity sensors
    i = getMIB(self.ip, ".1.3.6.1.4.1.3854.1.2.2.1.17.1.1")
    if (i != None):
      ids_humid = i

    v = getMIB(self.ip, ".1.3.6.1.4.1.3854.1.2.2.1.17.1.3")
    if (v != None):
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

    return zip(ids, values, units)
