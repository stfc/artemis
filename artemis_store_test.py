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

from artemis_store import session, Node, Probe

"""Minimal test suite and utilies for ARTEMIS data store"""

#testnode = Node("172.16.181.102", "xml_env_swift")
#session.merge(testnode)

#print(s.Probe("TEMPERATURE-1WIRE-000000FE0BEBDB", "25DD", 25, 31, 4, 2))

#print(session.dirty)

#print(session.query(Node).all())
#print(session.dirty)
#session.add(Probe("TEMPERATURE-1WIRE-000000FE0BEBDB", "25DD", 25, 31, 4, 2))

def convert():
  from artemis_config import base_nodes, sensors

  for b in base_nodes:
    c = str(b.__class__).split("'")[1].split(".")
    session.add(Node(b.ip, c[1], c[2]))

  for id, (n, x, y, w, h) in sensors.iteritems():
    session.add(Probe(id, n, x, y, w, h))

  session.commit()
