ARTEMIS
=======
Almost Real-Time Environmental Monitoring &amp; Information System


Getting Started
===============

If you've already got some environmental sensors, great! You're halfway there.

Check Supported Devices to see if your equipment is known to work.

If not, for most devices a plugin should not be difficult to write, see Plugin Development

If you are starting from scratch either buy some Supported Devices or take a look at Building Sensors.

Architecture
============

<pre>
    { sensors }->[ thread ]-.  [ crond ]
    { sensors }->[ thread ]-|       \
    { sensors }->[ thread ]-|->[ collector ]->/ json /->[ javascript ]->( display )
    { sensors }->[ thread ]-|        \
    { sensors }->[ thread ]-'   ( rrd files )
</pre>


Supported Devices
=================


This is not an exhaustive list, but devices listed have at least been tested once.

Some devices may be supported but not yet listed, check the git repository.

<table>
    <tr><th>Manufacturer</th><th>Model</th><th>Works</th><th>Protocol</th><th>Module</th></tr>
    <tr><td>SwiftTech</td><td>CM-2</td><td>Yes</td><td>XML</td><td>xml_env_swift</td></tr>
    <tr><td>SwiftTech</td><td>CM-2</td><td>Yes</td><td>SNMP</td><td>snmp_env_swift</td></tr>
    <tr><td>APC</td><td>AP7953</td><td>Yes</td><td>SNMP</td><td>snmp_pdu_apc</td></tr>
    <tr><td>Jacarta</td><td>Unknown</td><td>Unknown</td><td>SNMP</td><td>snmp_env_jacarta</td></tr>
</table>

Plugin Development
==================

Plugins for different sensors are implemented as individual modules in <code>nodetypes/</code>.

Each module is expected to define a class of the same name that subclasses <code>node</code> from <code>base.py</code> and as such must define at least one method (<code>fetch()</code>).
<pre>
  class node(object):
    def __init__(self, ip):
      self.ip        = ip
    def fetch(self):
      pass
</pre>

For plugins implementing access to SNMP devices, <code>base.py</code> also provides the convienience function <code>getMIB</code> for fetching the contents of MIB trees by walking the tree from a defined point.

<pre>
	getMIB(ip, mib, community = "public")
</pre>

In addition <code>base.py</code> provides the definitions for unit symbols and a lookup table for 1-Wire device families.

<pre>
	UNIT_TEMPERATURE
	UNIT_CURRENT
	UNIT_AIRFLOW
	UNIT_HUMIDITY

	FAMILY_1WIRE[]
</pre>

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

