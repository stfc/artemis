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

SOCKET_TIMEOUT = 10

from base import *

##
# 1-Wire Network attached monitoring base, using XML interface instead of SNMP
#
class node_swiftCM1_xml(node):
  def fetch(self):
    import xml.dom.minidom
    import socket
    from urllib2 import urlopen, URLError    
  
    SENSOR_TYPES = {
      "TempC"    : "TEMPERATURE",
      "Airflow"  : "AIRFLOW",
      "Humidity" : "HUMIDITY",
    }
  
    SENSOR_UNITS = {
      "TEMPERATURE" : UNIT_TEMPERATURE,
      "AIRFLOW"     : UNIT_AIRFLOW,
      "HUMIDITY"    : UNIT_HUMIDITY,  
    }
 
    socket.setdefaulttimeout(SOCKET_TIMEOUT)
    url = "http://" + self.ip + "/data.xml"
    try:
      url = urlopen(url)
    except URLError:
      print(self.ip + " timed out")

    if url:
      try:
        base = xml.dom.minidom.parse(url)
      except IOError:
        print("Could not grab data from " + self.ip + " - timed out")
        return([])
  
      devices = base.documentElement.getElementsByTagName('device')
  
      results = [] #Empty list to take tuples of (id, value, units)

      if len(devices) > 0:
        for device in devices:
          device_type = device.attributes["type"].nodeValue
          device_name = device.attributes["name"].nodeValue
          device_id   = device.attributes["id"].nodeValue
    
          if (device_type <> "MiniRSE"):
            device_id   = device_id[2:-2] + device_id[:2]
    
            for tag in device.childNodes:
              if tag.nodeName == "field":
                sensor_type = tag.attributes["key"].nodeValue
    
                if sensor_type in SENSOR_TYPES:
                  sensor_type  = SENSOR_TYPES[tag.attributes["key"].nodeValue]
                  sensor_value = tag.attributes["value"].nodeValue
                  results += [(("%s-1WIRE-%s" % (sensor_type, device_id)), sensor_value, SENSOR_UNITS[sensor_type])]

      return(results)
    else:
      return([])
