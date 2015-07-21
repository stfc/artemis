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

#Write event to debug log
f = open("artemis-debug-log.txt", "a")
f.write("Trap handler started\n")
f.close()

import sys, re

OID_NAMES = {
    "SNMPv2-MIB::snmpTrapOID.0"                 : "trap_oid",
    "DISMAN-EVENT-MIB::sysUpTimeInstance"       : "uptime",
    "SNMPv2-SMI::enterprises.12270.200.2.1.1.1" : "id",
    "SNMPv2-SMI::enterprises.12270.200.2.1.1.2" : "path", #might be wrong!
    "SNMPv2-SMI::enterprises.12270.200.2.1.1.3" : "timestamp",
    "SNMPv2-SMI::enterprises.12270.200.2.1.1.4" : "input",
    "SNMPv2-SMI::enterprises.12270.200.2.1.1.5" : "description",
    "SNMPv2-SMI::enterprises.12270.200.2.1.1.6" : "state",
    "SNMPv2-SMI::enterprises.12270.200.2.1.1.7" : "name",
#  "SNMPv2-SMI::enterprises.12270.200.2.1.1.8" : "item8", # Not sure what this is supposed to be
#  "SNMPv2-SMI::enterprises.12270.200.2.1.1.9" : "item9", # Not sure what this is either
    "SNMP-COMMUNITY-MIB::snmpTrapAddress.0"     : "ip",
    "SNMP-COMMUNITY-MIB::snmpTrapCommunity.0"   : "community",
}

#Pre-compile some regular expressions
re_clean             = re.compile(r'[\n"]')
re_description_value = re.compile(r'^\s*(.+?)\s*\[last value was\s*([0-9\.]+)\s*\]$')


#Read trap header
host = re_clean.sub("", sys.stdin.readline())
event_type = re_clean.sub("", sys.stdin.readline())

from datetime import datetime

#Write event to debug log
f = open("artemis-debug-log.txt", "a")
f.write("%s: Caught trap %s %s\n" % (datetime.now(), host, event_type))
f.close()

#Create empty dictionary for values
event = {}

#Parse trap data
for l in sys.stdin:
    oid, value = l.split(" ", 1)
    value = re_clean.sub("", value)

    if oid in OID_NAMES:
        #we know how to deal with this oid
        name = OID_NAMES[oid]
        if name == "description":
            #absolute values can be provided in [] in description by BMS, decode these
            m = re_description_value.match(value)
            if m:
                d, v = m.groups()
                event["description"] = d
                event["value"]       = v
            else:
                event[name] = value
        else:
            event[name] = value
    else:
        #this oid is unknown, do nothing with it
        pass

#Create event object
from artemis_trap_db import BMSEvent, setup
bms_event = BMSEvent(host, event_type, event)

#Write event to log
f = open("artemis-trap-log.txt", "a")
f.write(str(bms_event))
f.write("\n")
f.close()

#Write event to DB
s = setup()
s.add(bms_event)
s.commit()
s.close()
