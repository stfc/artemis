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

#Required modules from Python Standard Library
from time import clock
time_start = clock()
from datetime import datetime
import commands, os, sys

#Try to import rrdtool module
try:
  import rrdtool
except:
  print("ERROR: Unable to import the rrdtool module, is python-rrdtool installed?")
  sys.exit(1)

#Fall back to simplejson for versions of python < 2.5 (simplejson requires seperate install)
try:
  import json
except:
  try:
    import simplejson as json
  except:
    print("ERROR: Unable to find a usable json module, is simplejson installed?")
    sys.exit(1)

#ARTEMIS Components
from artemis_core import *
from nodetypes import base

#Load config module
from artemis_config import *

# Setup base nodes from store
base_nodes = []

for n in session.query(Node).all():
  base_nodes.append(load_class(n.module, n.object)(n.ip))

# Setup sensors from store
sensors = {}

for p in session.query(Probe).all():
  sensors[p.id] = [p.name, float(p.x), float(p.y), float(p.w), float(p.h)]

#Configuration
this_dir = os.path.dirname(os.path.realpath( __file__ )) + "/"
rrd_dir  = this_dir + config.get("rrd","dir")

print("Starting run...")

#Start collection
g = grabData(base_nodes)

snapshot_list = [];

print("---- Data grab complete ----")

for serial, value, units, name in g:
  print(r"%2.3f : Found sensor %s with value %s %s and name %s" % (clock(), serial, value, units, name))
  rrd = str(rrd_dir + serial + config.get("rrd","ext"))

  if not os.path.isfile(rrd):
    #create rrd if none exists
    print("Creating new RRD " + rrd)
    rrdtool.create(
      rrd,
      "--step", "60",
      "DS:val:GAUGE:120:-100:100", # Accept data between -100 and +100 as valid
      "RRA:AVERAGE:0.5:1:525600", # A year of minutes
      "RRA:AVERAGE:0.5:60:8760", # A year of hours
      "RRA:MAX:0.5:60:8760", # A year of hours
      "RRA:MIN:0.5:60:8760", # A year of hours
    )

  #update data
  rrdtool.update(rrd, "N:" + str(value))

  #store latest values
  try:
    (n, x, y, h, w) = sensors[serial]
  except:
    (n, x, y, h, w) = ("Auto-detected " + name, 0, 0, 0, 0)
    session.add(Probe(serial, n, x, y, h, w))

  # Update timestamp
  probe = session.query(Probe).filter(Probe.id == serial).first()
  if (probe.name <> n):
    print("Mismatch of name against node %s vs %s" % (probe.name, n))
  probe.lastcontact = datetime.now()

  row = [serial, value, n, x, y, h, w]

  snapshot_list.append(row)

# Commit outside loop
session.commit()

# Prep config
c = dict(config.items("room"))
c["tile_size"] = int(c["tile_size"])
c["offset_x"] = int(c["offset_x"])
c["offset_y"] = int(c["offset_y"])

#Dump data
dump_prep = {
  "config" : c,
  "probes" : snapshot_list,
}


# Write out data dump for gui
try:
  file_json_dump = open(this_dir + "data/data-dump.json", "w")
  json.dump(dump_prep, file_json_dump)
  file_json_dump.close()
  print("Wrote output to %s" % file_json_dump.name) 
except:
  print("Error while writing data dump file - %s %s %s" % sys.exc_info())


# Update performance rrd
rrd = str(rrd_dir + "ARTEMIS-STATS-" + c["name"].replace(" ","_") + config.get("rrd","ext"))

if not os.path.isfile(rrd):
  #create rrd if none exists
  print("Creating new RRD " + rrd)
  rrdtool.create(
    rrd,
    "--step", "60",
    "DS:collect:GAUGE:120:0:3600", # Accept data between 0 and 3600 as valid
    "DS:nodes:GAUGE:120:0:U", # Number of known nodes
    "DS:probes:GAUGE:120:0:U", # Number of known probes
    "RRA:AVERAGE:0.5:1:525600", # A year of minutes
    "RRA:AVERAGE:0.5:60:8760", # A year of hours
    "RRA:MAX:0.5:60:8760", # A year of hours
    "RRA:MIN:0.5:60:8760", # A year of hours
  )

time_run = clock() - time_start

rrdtool.update(rrd, "N:%f:%d:%d" % (time_run, len(base_nodes), len(g)))
print("Collect finished in %0.3f seconds" % (time_run))

