ARTEMIS
=======

Almost Real-Time Environmental Monitoring &amp; Information System


Getting Started
===============

If you've already got some environmental sensors, great! You're halfway there.

Check Supported Devices to see if your equipment is known to work.

If not, for most devices a plugin should not be difficult to write, see Plugin Development

If you are starting from scratch either buy some Supported Devices or take a look at Building Sensors.

Prerequisites
-------------

* httpd
* php
* python 2.6+
* python-rrdtool
* rrdtool
* python-sqlalchemy
* python-argparse

Installation
------------

1. Run `setup.sh` to initialise config files and storage directories.
2. Edit `artemis.conf` to your liking.
3. Run `./artemis_collect.py` to initialise the data store.
4. Add at least one node using `artemis_cli.py add_node`.
5. Run `./artemis_collect.py` to detect and collect data from probes.
6. Update positions of probes using `artemis_cli.py update_probe`.
7. If necessary, modify `artemis.cron`and copy to `/etc/cron.d/`.


Architecture
============

    { sensors }->[ thread ]-.    [ crond ]
    { sensors }->[ thread ]-|        :
    { sensors }->[ thread ]-|->[ collector ]->/ json /->[ javascript ]->( display )
    { sensors }->[ thread ]-|        |
    { sensors }->[ thread ]-'  ( rrd files )


Supported Devices
=================

This is not an exhaustive list, but devices listed have at least been tested once.

Some devices may be supported but not yet listed, check the git repository.

<table>
    <tr><th>Manufacturer</th><th>Model</th><th>Works</th><th>Protocol</th><th>Module</th></tr>
    <tr><td>SwiftTech</td><td>CM-2</td><td>✓</td><td>XML</td><td>xml_env_swift</td></tr>
    <tr><td>SwiftTech</td><td>CM-2</td><td>✓</td><td>SNMP</td><td>snmp_env_swift</td></tr>
    <tr><td>APC</td><td>AP7953</td><td>✓</td><td>SNMP</td><td>snmp_pdu_apc</td></tr>
    <tr><td>Jacarta</td><td>Unknown</td><td>?</td><td>SNMP</td><td>snmp_env_jacarta</td></tr>
</table>


Plugin Development
==================

Plugins for different sensors are implemented as individual modules in `nodetypes/`.

Each module is expected to define a class of the same name that subclasses `node` from `base.py` and as such must define at least one method (`fetch()`).

```python
class node(object):
    def __init__(self, ip):
        self.ip = ip
    def fetch(self):
        pass
```

For plugins implementing access to SNMP devices, `base.py` also provides the convenience function `getMIB` for fetching the contents of MIB trees by walking the tree from a defined point.

```python
getMIB(ip, mib, community = "public")
```

In addition `base.py` provides the definitions for unit symbols and a lookup table for 1-Wire device families.

```python
UNIT_TEMPERATURE
UNIT_CURRENT
UNIT_AIRFLOW
UNIT_HUMIDITY

FAMILY_1WIRE[]
```

Additional unit definitions and 1-wire families should be added as needed.


Reference Platform
==================

1-Wire Sensors
--------------
Maxim 1-Wire sensors are low-cost, readily available and accurate devices which can easily be interfaced to a computer with USB or other interfaces.

* DS1822
    * Temperature
    * &plusmn;2C
    * 9-12 bit
* DS18B20
    * Temperature
    * &plusmn;0.5C
    * 9-12 bit
* DS18S20
    * Temperature
    * &plusmn;0.5C
    * 9 bit

Base Units
----------
There is currently an ongoing project to develop a low-cost base unit around the Raspberry Pi which when completed will be our recommended base unit.

For the time being, other good options are low cost development boards and systems based around a VIA or Atom CPU, many of which are available for under &pound;100.
Or existing commercial units which cost in the region of &pound;500.

