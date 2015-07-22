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

import argparse
import logging
import json

from sys import exit as sys_exit

# Load artemis modules
from artemis_core import load_plugin
from artemis_config import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["add_node", "remove_node", "list_nodes", "list_probes", "update_probe"])
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--format", choices=["json"])
    opts, args = parser.parse_known_args()

    logger = logging.Logger("artemis_cli")
    logger.setLevel(logging.INFO)
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(logging.Formatter("%(levelname)8s: %(message)s"))
    logger.addHandler(log_handler)

    if opts.debug:
        logger.setLevel(logging.DEBUG)


    logger.debug("global opts: %s", opts)
    logger.debug("global args: %s", args)


    if opts.action == "add_node":
        logger.debug("action: add_node")
        p = argparse.ArgumentParser(usage="%(prog)s add_node IP PLUGIN [-u USERNAME] [-p PASSWORD]")
        p.add_argument("ip")
        p.add_argument("plugin")
        p.add_argument("-u", "--username")
        p.add_argument("-p", "--password")
        o, a = p.parse_known_args(args)

        logger.debug("action opts: %s", o)
        logger.debug("action args: %s", a)

        if o.ip and o.plugin:
            try:
                load_plugin(o.plugin)
            except ImportError:
                logger.error("%s is not a valid plugin", o.plugin)
                sys_exit(1)

            node = Node(o.ip, o.plugin)
            try:
                session.add(node)
                node.username = o.username
                node.password = o.password
                session.commit()
                logger.info("Node added")
            except IntegrityError:
                logger.error("Node already exists")
                sys_exit(1)


    elif opts.action == "remove_node":
        logger.debug("action: remove_node")
        p = argparse.ArgumentParser(usage="%(prog)s remove_node IP")
        p.add_argument("ip")
        o, a = p.parse_known_args(args)

        logger.debug("action opts: %s", o)
        logger.debug("action args: %s", a)

        if o.ip:
            node = session.query(Node).filter(Node.ip == o.ip).first()
            if node:
                session.delete(node)
                session.commit()
                logger.info("Node removed")
            else:
                logger.error("No node found with the IP %s", o.ip)


    elif opts.action == "list_nodes":
        logger.debug("action: list_nodes")
        nodes = session.query(Node).all()
        if opts.format == "json":
            o = []
            for n in nodes:
                o.append(n.list())
            o = { "aaData" : o }
            print(json.dumps(o))
        else:
            for n in nodes:
                print(n)


    elif opts.action == "update_probe":
        logger.debug("action: update_probe")
        p = argparse.ArgumentParser(usage="%(prog)s update_probe [options]")
        p.add_argument("id", help="probe id")
        p.add_argument("-n", help="name")
        p.add_argument("-x", help="x position")
        p.add_argument("-y", help="y position")
        p.add_argument("-z", help="z position")
        p.add_argument("-w", help="width")
        p.add_argument("-d", help="depth")
        p.add_argument("-t", help="height")
        o, a = p.parse_known_args(args)

        logger.debug("action opts: %s", o)
        logger.debug("action args: %s", a)

        if o.n is o.x is o.y is o.z is o.w is o.d is o.t is None:
            p.print_help()

        else:
            probe = session.query(Probe).filter(Probe.id == o.id).first()

            # Try name if id doesn't match any probes
            if not probe:
                logger.info("No probe found with id '%s', trying to match by name", o.id)
                probe = session.query(Probe).filter(Probe.name == o.id).all()

                if len(probe) > 1:
                    logger.error("%d probes found with the name '%s', use ID to update each in turn", len(probe), o.id)
                    for p in probe:
                        print p
                    sys_exit(1)

                probe = probe[0]

            if probe:
                if o.n:
                    probe.name = o.n
                if o.x:
                    probe.x = o.x
                if o.y:
                    probe.y = o.y
                if o.z:
                    probe.z = o.z
                if o.w:
                    probe.w = o.w
                if o.t:
                    probe.h = o.t
                if o.d:
                    probe.d = o.d

                session.commit()
                logger.info("Probe updated")
            else:
                logger.error("No probe found with id or name '%s'", o.id)


    elif opts.action == "list_probes":
        logger.debug("action: list_probes")
        probes = session.query(Probe).all()
        if opts.format == "json":
            o = []
            for p in probes:
                o.append(p.list())
            o = { "aaData" : o }
            print(json.dumps(o))
        else:
            for p in probes:
                print(p)


    else:
        print("Unimplemented action")
