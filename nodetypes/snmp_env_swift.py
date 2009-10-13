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

from base import *

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
