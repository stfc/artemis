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

from threading import Thread

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
#    print("INFO: Called fetch() on " + self.node.ip)
    if (data != None):
      self.data = data
#      print("  OK: Got data from " + self.node.ip)
    else:
      print("  WARNING: Got no data from " + self.node.ip)

#Import all defined datasource nodes
from nodetypes import *

