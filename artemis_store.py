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

"""Classes and functions related to the ARTEMIS object data store"""

# Load and replace standard Python decimal library with the faster cdecimal library
#import sys
#import cdecimal
#sys.modules["decimal"] = cdecimal

# Load core dependencies
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Numeric, String, DateTime
from datetime import datetime

Base = declarative_base()

class Node(Base):
  """Properties of a interrogatable sensor unit"""

  __tablename__ = 'nodes'
  ip = Column(String(16), primary_key=True)
  module = Column(String(16))
  object = Column(String(16))
  lastcontact = Column(DateTime())

  def __init__(self, ip, module, object):
      self.ip = ip
      self.module = module
      self.object = object
      self.lastcontact = datetime.now()
  
  def __repr__(self):
      return "<Unit (%s, %s, %s)>" % (self.ip, self.module, self.object)


class Probe(Base):
  """Properties of a sensor endpoint"""

  __tablename__ = 'probes'
  id = Column(String(64), primary_key=True)
  name = Column(String(64)) # Locally defined name
  #remote_name = Column(String(64)) # Name on remote device
  #node = Column(String(16)) # Node this probe was last seen on
  #state = Column(Byte()) # Discovery state
  x = Column(Numeric(2))
  y = Column(Numeric(2))
  w = Column(Numeric(2))
  h = Column(Numeric(2))
  lastcontact = Column(DateTime())

  def __init__(self, id, name, x, y, w, h):
      self.id = id
      self.name = name
      self.x = x
      self.y = y
      self.w = w
      self.h = h
      self.lastcontact = datetime.now()

  def __repr__(self):
      return "<Probe %s : (%s, %d.2, %d.2, %d.2, %d.2)>" % (self.id, self.name, self.x, self.y, self.w, self.h)


engine = create_engine('sqlite:///artemis_store.db', echo=False)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()
