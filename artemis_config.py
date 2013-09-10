#!/usr/bin/python26
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

import ConfigParser

#Depends on node classes from artemis_core
from nodetypes.snmp_env_jacarta import *
from nodetypes.snmp_env_swift import *
from nodetypes.snmp_pdu_apc import *
from nodetypes.xml_env_swift import *

from artemis_store import session, Node, Probe

config = ConfigParser.ConfigParser()
config.read(['artemis.conf.defaults', 'artemis.conf'])
