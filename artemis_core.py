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

from threading import Thread
from time import time

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
    if grabber.data:
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
    start_time = time()
    data = self.node.fetch()
    end_time = time()
    print("Fetch on %s %s (%s) ran for %f seconds" % (self.node.ip, self.node.__class__, self._Thread__name, end_time-start_time))
    if data:
      self.data = [d + (self.node.ip,) for d in data] # Concatenate source node back onto each record

def load_plugin(plugin):
  m = __import__("nodetypes.%s" % (plugin))
  c = getattr(getattr(m, plugin), 'node')
  return(c)
