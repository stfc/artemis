#!/usr/bin/env python

import json, urllib2, datetime


def process(d, f):
  x = []
  y = []
  z = []
  
  for i in d:
    if "TEMPERATURE" in i[0]:
      if "Row " in i[2]:
        r = float(i[3])
        c = float(i[4])
        v = float(i[1])
  
        x.append(r)
        y.append(c)
        z.append(v)

  plot(x, y, z, "R89 HPD Room", f)

  

def plot(x, y, z, title, filename):
  import numpy as np
  from matplotlib.mlab import griddata
  
  w = max(x) - min(x)
  h = max(y) - min(y)
  
  xi = np.linspace(min(x), max(x), w * 4)
  yi = np.linspace(min(y), max(y), h * 4)
  
  zi = griddata(x,y,z,xi,yi)
  
  x = np.array(x)
  y = np.array(y)
  z = np.array(z)
  
  
  import matplotlib.pyplot as plt
  
  plt.scatter(x,y,marker='o',c='b',s=5,zorder=10)
  #CS = plt.contour(xi,yi,zi,15,linewidths=0.5,colors='k')
  #CS = plt.contourf(xi,yi,zi,15,cmap=plt.cm.jet)
  plt.pcolor(xi,yi,zi)
  plt.clim(15,38)
  ax = plt.axes()
  ax.set_aspect('equal')
  plt.xlim(min(x), max(x))
  plt.ylim(max(y), min(y))

  plt.suptitle(title)
  
  plt.colorbar()
  
  f = "hm/hm_%s.png" % filename
  plt.savefig(f)
  print("Wrote " + f)
  plt.clf()




MODE = 1

if MODE == 0:
  p = urllib2.urlopen("http://thor.gridpp.rl.ac.uk/r89-hpd/data/data-dump.json")
  p = json.load(p)
  p = p["probes"]
  process(p, "dump")

elif MODE == 1:
  p = urllib2.urlopen("http://thor.gridpp.rl.ac.uk/r89-hpd/artemis_dump.php")
  p = json.load(p)

  (time_start, period, time_end, p) = p
  time_start = int(time_start)
  period     = int(period)
  time_end   = int(time_end)

  for t in p.items():
    (t,rv) = t

    x = []
    y = []
    z = []

    for r in rv:
      (r,c,v) = r

      if v <> None:
        x.append(float(r))
        y.append(float(c))
        z.append(float(v))

    if (len(x) == len(y)) and (len(x) == len(z)) and (len(x) > 0):
      plot(x, y, z, "R89 HPD Room at %s" % datetime.datetime.fromtimestamp(time_start + period * int(t)).strftime("%Y-%m-%d %H:%M:%S"), "%05d" % int(t))

else:
  import sys
  sys.exit("ERROR: Unknown run mode")

