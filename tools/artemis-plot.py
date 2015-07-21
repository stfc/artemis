#!/usr/bin/env python
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

import urllib2, datetime

#Fall back to simplejson for versions of python < 2.5 (simplejson requires seperate install)
try:
    import json
except:
    try:
        import simplejson as json
    except:
        sys.exit("ERROR: Unable to find a usable json module, is simplejson installed?")


TEMP_MIN = 15
TEMP_MAX = 38
DPI = 106

from pylab import *
cdict = {
    'red'   : ((0.0, 0.1, 0.1), (0.25, 0.0, 0.0), (0.5, 1.0, 1.0), (0.75, 1.0, 1.0), (1.0, 1.0, 1.0)),
    'green' : ((0.0, 0.1, 0.1), (0.25, 0.0, 0.0), (0.5, 0.0, 0.0), (0.75, 1.0, 1.0), (1.0, 1.0, 1.0)),
    'blue'  : ((0.0, 0.1, 0.1), (0.25, 0.5, 0.5), (0.5, 0.0, 0.0), (0.75, 0.0, 0.0), (1.0, 1.0, 1.0)),
}
my_cmap = matplotlib.colors.LinearSegmentedColormap('my_colormap',cdict,256)
#pcolor(rand(10,10),cmap=plt.cm.jet)

def process(d, f, mode):
    x = []
    y = []
    z = []

    for i in d:
        if "TEMPERATURE" in i[0]:
            r = float(i[3])
            c = float(i[4])
            v = float(i[1])

            x.append(r)
            y.append(c)
            z.append(v)

    plot(x, y, z, "R89 HPD Room", f, mode)

def plot(x, y, z, title, filename, mode):
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
    CS = plt.contourf(xi,yi,zi,15,cmap=plt.cm.jet)
    plt.pcolor(xi,yi,zi,cmap=plt.cm.jet)
    plt.colorbar()
    plt.clim(TEMP_MIN, TEMP_MAX)
    ax = plt.axes()
    ax.set_aspect('equal')
    plt.xlim(min(x), max(x))
    plt.ylim(max(y), min(y))


    if mode == "range":
        f = "hm/hm_%s.png" % filename
    else:
        f = filename

    if mode == "gui":
        plt.show()
        plt.suptitle(title)
        plt.colorbar()
    else:
        for a in ax.get_xticklabels():
            a.set_visible(False)
        for a in ax.get_yticklabels():
            a.set_visible(False)

        plt.savefig(f, dpi=DPI)
        print("Wrote " + f)

    plt.clf()


if __name__ == "__main__":
    from optparse import OptionParser

    VERSION = "1.0"

    p = OptionParser(version=VERSION)

    p.usage = "    %prog URL [options]"

    p.description = "A utility to plot heatmaps from artemis probe data."

    p.add_option("--mode", metavar="STR", dest="mode", default="single", help="Run mode (single, gui or range)")
    p.add_option("--filename", metavar="STR", dest="filename", default="heatmap.png", help="Output filename (ignored in gui and range modes)")

    (o, a) = p.parse_args()

    if len(a) == 1:
        url = a[0]

        p = urllib2.urlopen(url)
        p = json.load(p)

        if o.mode == "gui" or o.mode == "single":
            p = p["probes"]
            process(p, o.filename, o.mode)

        elif o.mode == "range":
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
                    plot(x, y, z, "R89 HPD Room at %s" % datetime.datetime.fromtimestamp(time_start + period * int(t)).strftime("%Y-%m-%d %H:%M:%S"), "%05d" % int(t), o.mode)

        else:
            import sys
            sys.exit("ERROR: Unknown run mode")
    else:
        import sys
        sys.exit("ERROR: URL not specified")
