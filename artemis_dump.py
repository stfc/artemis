#!/usr/bin/env python
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

import artemis_config

RRD_DIR = "/home/apache/html/r89-hpd/rrds/"

#Fall back to simplejson for versions of python < 2.5 (simplejson requires seperate install)
try:
    import json
except:
    try:
        import simplejson as json
    except:
        print("ERROR: Unable to find a usable json module, is simplejson installed?")
        sys.exit(1)

import sys, time, rrdtool

# Provide list of valid sensors if none specified
if len(sys.argv) == 1:
    sensors = artemis_config.sensors.keys()
else:
    sensors = sys.argv[1:]

results = {}
times   = {}

time_start_min = int(time.time())
time_end_max   = 0

sensormap   = {}
sensorcount = 0

for sensor in sensors:
    if ("TEMPERATURE" in sensor) and ("Row" in artemis_config.sensors[sensor][0]):
        sensorcount = sensorcount + 1
        sensormap[sensorcount] = 0
        (x, y) = artemis_config.sensors[sensor][1:3]
        rrd = RRD_DIR + sensor + ".rrd"
        data = rrdtool.fetch(rrd, "AVERAGE", "-s", "-2d", "-e" "-1d")
        ((time_start, time_end, period), (name), (data)) = data

        time_start_min = min(time_start_min, time_start)

        time_end_max = max(time_end_max, time_end)

        time = 0
        results[sensorcount] = {}

        for r in data:
            time = time + 1
            times[time] = 1

            z = r[0]

            if (z <> None):
                z = str(round(z, 2))

            results[sensorcount][time] = [str(round(x, 2)), str(round(y, 2)), z]

        if (time * period <> time_end - time_start):
            print("Bad stuff happened")

times = times.keys()
times.sort()

output = {}

for time in times:
    output[time] = []
    for i in sensormap.keys():
        output[time].append(results[i][time])

print(json.dumps([time_start_min, period, time_end_max ,output]))
