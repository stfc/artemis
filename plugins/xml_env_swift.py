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

SOCKET_TIMEOUT = 20

from time import clock
from base import *

##
# 1-Wire Network attached monitoring base, using XML interface instead of SNMP
#
class node(node):
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
      res = urlopen(url)
      #print("%2.3f %s %s" % (clock(), url, str(res))) #debug
      base = xml.dom.minidom.parse(res)

      devices = base.documentElement.getElementsByTagName('device')
      device_count = len(devices)

      results = [] #Empty list to take tuples of (id, value, units, name)

      if device_count > 0:
        for device in devices:
          device_type = device.attributes["type"].nodeValue
          device_name = device.attributes["name"].nodeValue
          device_id   = device.attributes["id"].nodeValue
          device_up   = device.attributes["available"].nodeValue

          if (device_up and (device_type <> "MiniRSE")):
            device_id   = device_id[2:-2] + device_id[:2]

            for tag in device.childNodes:
              if tag.nodeName == "field":
                sensor_type = tag.attributes["key"].nodeValue

                if sensor_type in SENSOR_TYPES:
                  sensor_type  = SENSOR_TYPES[tag.attributes["key"].nodeValue]
                  sensor_value = tag.attributes["value"].nodeValue
                  results += [(("%s-1WIRE-%s" % (sensor_type, device_id)), sensor_value, SENSOR_UNITS[sensor_type], device_name)]
                else:
                  print("%2.3f\t%s Ignoring sensor with type: %s" % (clock(), url, sensor_type))
          else:
            print(url + " Found base unit")
        print("%2.3f\t%s found %d attached devices" % (clock(), url, device_count))
        return(results)
      else:
        print("%2.3f\t%s No attached devices found" % (clock(), url))
        return([])
    except URLError:
      print("%2.3f\tCould not grab data from %s - URLError" % (clock(), url))
      return([])
    except IOError:
      print("%2.3f\tCould not grab data from %s - IOError" % (clock(), url))
      return([])
    except:
      print("%2.3f\tCould not grab data from %s - Unknown Exception" % (clock(), url))
      return([])
    return([]) #Backstop
