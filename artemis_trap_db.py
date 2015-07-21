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

from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData, ForeignKey

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BMSEvent(Base):
    __tablename__ = "bms_events"

    id          = Column(Integer, primary_key=True)
    host        = Column(String)
    type        = Column(String)
    trap_oid    = Column(String)
    uptime      = Column(String)
    path        = Column(String)
    timestamp   = Column(String)
    input       = Column(String)
    description = Column(String)
    value       = Column(String)
    state       = Column(String)
    name        = Column(String)
    ip          = Column(String)

    def __init__(self, host, type, values):
        self.host        = host
        self.type        = type
        self.id          = values["id"]
        self.trap_oid    = values["trap_oid"]
        self.uptime      = values["uptime"]
        self.path        = values["path"]
        self.timestamp   = values["timestamp"]
        self.input       = values["input"]
        self.description = values["description"]
        self.value       = values["value"]
        self.state       = values["state"]
        self.name        = values["name"]
        self.ip          = values["ip"]

    def __repr__(self):
        return "<BMSEvent(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)>" % (self.id, self.host, self.type, self.trap_oid, self.uptime, self.path, self.timestamp, self.input, self.description, self.value, self.state, self.name, self.ip)


def setup():
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///artemis_traps.sqlite', echo=True)

    BMSEvent.metadata.create_all(engine)

    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)

    session = Session()

    return session

def test(session):
    v = {
        "id"          : "12345",
        "uptime"      : "8:22:31:15.52",
        "trap_oid"    : "SNMPv2-SMI::enterprises.12270.0.32",
        "path"        : "/L00/O99",
        "timestamp"   : "2010-01-07T00:00:00",
        "input"       : "A01",
        "description" : "Clear Digital Input",
        "value"       : "0.00",
        "state"       : "TST1",
        "name"        : "Test Event",
        "ip"          : "127.0.0.1",
    }
    test_event = BMSEvent("UDP: [127.0.0.1]:161", "<TEST>", v)
    session.add(test_event)
    session.commit()
