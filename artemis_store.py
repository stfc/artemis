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

"""Classes and functions related to the ARTEMIS object data store"""

# Load and replace standard Python decimal library with the faster cdecimal library
#import sys
#import cdecimal
#sys.modules["decimal"] = cdecimal

import json

import ConfigParser
config = ConfigParser.ConfigParser()
config.read(['artemis.conf'])

# Load core dependencies
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, Integer, String, DateTime
from datetime import datetime

Base = declarative_base()

class Node(Base):
  """Properties of a interrogatable sensor unit"""

  __tablename__ = 'nodes'
  ip = Column(String(16), primary_key=True)
  plugin = Column(String(16))
  lastcontact = Column(DateTime())

  def __init__(self, ip, plugin):
      self.ip = ip
      self.plugin = plugin
      self.lastcontact = datetime.now()

  def __repr__(self):
      return "<Node (%s, %s)>" % (self.ip, self.plugin)

  def list(self):
      l = []
      l.append(self.ip)
      l.append(self.plugin)
      l.append(self.lastcontact.isoformat(" "))
      return(l)


class Probe(Base):
  """Properties of a sensor endpoint"""

  __tablename__ = 'probes'
  id = Column(String(64), primary_key=True)
  name = Column(String(64)) # Locally defined name

  # Position
  x = Column(Float(2))
  y = Column(Float(2))
  z = Column(Float(2))

  # Dimensions
  w = Column(Float(2))
  d = Column(Float(2))
  h = Column(Float(2))

  # Guidance
  remote_name = Column(String(64)) # Name on remote device
  node = Column(String(16)) # Node this probe was last seen on
  state = Column(Integer()) # Discovery state
  lastcontact = Column(DateTime()) # Timestamp of last reading

  def __init__(self, id, name, x, y, z, w, h, d):
      self.id = id
      self.name = name

      self.x = x
      self.y = y
      self.z = z

      self.w = w
      self.h = h
      self.d = d

      self.remote_name = ""
      self.node = ""
      self.state = 0
      self.lastcontact = datetime.now()

  def __repr__(self):
      return "<Probe %s : (%s, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %s, %s, %s, %s)>" % (self.id, self.name, self.x, self.y, self.z, self.w, self.d, self.h, self.remote_name, self.node, self.state, self.lastcontact)

  def list(self):
      l = []
      l.append(self.id)
      l.append(self.name)
      l.append(self.x)
      l.append(self.y)
      l.append(self.z)
      l.append(self.w)
      l.append(self.h)
      l.append(self.d)
      l.append(self.lastcontact.isoformat(" "))
      l.append(self.node)
      l.append(self.remote_name)
      return(l)



engine = create_engine(config.get("store","connection_string"), echo=False)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()
