#!/usr/bin/env python

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

DATA_SOURCE_URL = "http://thor.gridpp.rl.ac.uk/artemis/data/probe-data.json" #Location of data source


#Required modules from Python Standard Library
import sys, urllib

#Fall back to simplejson for versions of python < 2.5 (simplejson requires seperate install)
try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        sys.exit("ERROR: Unable to find a usable json module, is simplejson installed?")



if len(sys.argv) == 2:                                  #Make sure an id has been provided
    data_source = urllib.urlopen(DATA_SOURCE_URL)         #Open the data source
    data_source = json.load(data_source)                  #Decode the JSON into a list of list

    data = {}                                             #Initialise new dictionary

    for r in data_source:                                 #Fill the dictionary with the sensor values with the id as the key
        (sensor_id, value, alias, row, column, width, height) = r
        data[sensor_id] = value

    try:                                                  #Return requested id, or fail gracefully
        print(data[sys.argv[1]])
    except IndexError:
        sys.exit("Probe ID not found")
else:
    sys.exit("USAGE: artemis-get.py PROBE_ID")
