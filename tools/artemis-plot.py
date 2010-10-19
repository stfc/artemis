#!/usr/bin/env python

import json, urllib2

d = urllib2.urlopen("http://thor.gridpp.rl.ac.uk/r89-hpd/data/data-dump.json")
d = json.load(d)

c = d["config"]
d = d["probes"]

data = []
cols = {}

for i in d:
  if "TEMPERATURE" in i[0]:
    if "Row " in i[2]:
      p = i[2].split()
      r = float(p[1]) * 2
      c = float(p[3])
      v = float(i[1])
      if p[2] == "Hot":
        r = r + 1

      data.append([r,c,v])
      cols[c] = 0

data.sort()

cols = len(cols)
rows = len(data) / cols

grid = []

for i in range(0, rows):
  j = i * cols
  grid.append([k[2] for k in data[j:j + cols]])
  grid.append([0 for k in range(0, cols)])

grid = grid[:-1]

for i in range(1,rows*2-1,2):
  for j in range(0,cols):
    grid[i][j] = (grid[i-1][j] + grid[i+1][j]) / 2

import numpy as np

grid.reverse()
grid = np.array(grid)


import matplotlib.pyplot as plt

plt.pcolor(grid)
plt.colorbar()
plt.show()
