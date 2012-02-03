#!/usr/bin/env python

#The MIT License
#
# Copyright (c) 2007 Nick Galbreath
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

#
# Version 2 - 12-Sept-2007 Simplified XML output
#                          Added commandline interface
# Version 1 - 10-Sept-2007 Initial release
#

from math import *

#
# Convert (x,y,z) on unit sphere
# back to (long, lat)
#
# p is vector of three elements
# 
def toEarth(p):
    if (p[0] == 0.0):
        longitude = pi / 2.0
    else:
        longitude = atan(p[1]/p[0])
    colatitude = acos(p[2]);
    latitude = (pi / 2.0 - colatitude)

    # select correct branch of arctan
    if p[0] < 0.0:
        if p[1] <= 0.0:
            longitude = -(pi - longitude)
        else:
            longitude = pi + longitude

    DEG = 180.0 / pi
    return [longitude * DEG, latitude * DEG]

#c
# convert long, lat IN RADIANS to (x,y,z)
# 
def toCart(longitude, latitude):
    theta = longitude
    # spherical coordinate use "co-latitude", not "lattitude"
    # lattiude = [-90, 90] with 0 at equator
    # co-latitude = [0, 180] with 0 at north pole
    phi = pi / 2.0 - latitude
    return [ cos(theta) * sin(phi), sin(theta) * sin(phi), cos(phi)]

# spoints -- get raw list of points in long,lat format
#
# meters: radius of polygon
# n: number of sides
# offset: rotate polygon by number of degrees
#
# Returns a list of points comprising the object
#
def spoints(long, lat, meters, n, offset=0):
    # constant to convert to radians
    RAD = pi / 180.0;
    # Mean Radius of Earth, meters
    MR = 6378.1 * 1000.0;
    offsetRadians = offset * RAD
    # compute longitude degrees (in radians) at given latitude
    r = (meters / (MR * cos(lat * RAD)))

    vec = toCart(long * RAD, lat * RAD)
    pt = toCart(long * RAD + r, lat * RAD)
    pts = [ ]

    for i in range(0,n):
        pts.append(toEarth(rotPoint(vec, pt, offsetRadians + (2.0 * pi/n)*i)))

    # connect to starting point exactly
    # not sure if required, but seems to help when
    # the polygon is not filled
    pts.append(pts[0])
    return pts

#
# rotate point pt, around unit vector vec by phi radians
# http://blog.modp.com/2007/09/rotating-point-around-vector.html
# 
def rotPoint(vec, pt,  phi):
    # remap vector for sanity
    (u,v,w,x,y,z) = (vec[0],vec[1],vec[2], pt[0],pt[1],pt[2])

    a = u*x + v*y + w*z;
    d = cos(phi);
    e = sin(phi);

    return [ (a*u + (x - a*u)*d + (v*z - w*y) * e),
             (a*v + (y - a*v)*d + (w*x - u*z) * e),
             (a*w + (z - a*w)*d + (u*y - v*x) * e) ]

#
# Regular polygon
# (longitude, latitude) in decimal degrees
# meters is radius in meters
# segments is number of sides, > 20 looks like a circle
# offset, rotate polygon by a number of degrees
#
# returns a string suitable for adding to a KML file.
#
# You may want to
#  edit this function to change "extrude" and other XML nodes.
#
def kml_regular_polygon(long, lat, meters, segments=30, offset=0):
    s = "<Polygon>\n"
    s += "  <outerBoundaryIs><LinearRing><coordinates>\n"
    for p in spoints(long, lat, meters, segments, offset):
        s += "    " + str(p[0]) + "," + str(p[1]) + "\n"
    s += "  </coordinates></LinearRing></outerBoundaryIs>\n"
    s += "</Polygon>\n"
    return s

#
# Make a "star" or "burst" pattern
#
# (long, lat) = center point
# outer = radius in meters
# inner = radius in meters, typically < outer
# segments = number of "points" on the star
# offset = rotate by degrees
#
# Returns a XML snippet suitable for adding into a KML file
#
def kml_star(long, lat, outer, inner, segments=10, offset=0):
    opts = spoints(long, lat, outer, segments, offset)
    ipts = spoints(long, lat, inner, segments, offset + 180.0 / segments)

    # interweave the outer and inner points
    # I'm sure there is a better way
    pts = []
    for i in range(len(opts)):
        pts.append(opts[i])
        pts.append(ipts[i])

    s = "<Polygon>\n"
    s += "  <outerBoundaryIs><LinearRing><coordinates>\n"
    for p in pts:
        s += "    " + str(p[0]) + "," + str(p[1]) + "\n"
    s += "  </coordinates></LinearRing></outerBoundaryIs>\n"
    s += "</Polygon>\n"
    return s

#    s += "  <extrude>1</extrude>\n"
#   s += "  <altitudeMode>clampToGround</altitudeMode>\n"


#
# The rest is only for command line argument 
# processing
#

import sys
import getopt

def usage(code, msg):

    u = """
-h, --longitude longitude in degrees (h is for 'horizontal')
-v, --latitude  latitude in degrees (v is for 'vertical')
-r, --radius    radius in meters
-s, --sides     number of sides
-i, --inner     optional, inner radius in meters,  default same as 'radius'
                this will make a 'star'
-o, --offset    optional, rotate polygon by angle in degrees, default 0
-?, --help      this usage

"""
    sys.stderr.write(msg)
    sys.stderr.write("\n\n")
    sys.stderr.write(u)
    sys.exit(code)


def main(argv):
    longitude = ""
    latitude = ""
    radius = ""
    sides = ""
    inner = ""
    offset = 0

    try:
        opts, args = getopt.getopt(argv, "h:v:r:s:i:o:",
                                   ["longitude", "latitude", "radius", "sides",
                                    "inner", "offset"])
    except getopt.GetoptError:
        usage(1, "Unknown option!");
    
    if len(opts) == 0:
        usage(1, "help")
    for opt, arg in opts:
        if opt in ("-h", "--longitude"):
            longitude = float(arg)
        elif opt in ("-v", "--latitude"):
            latitude = float(arg)
        elif opt in ("-r", "--radius"):
            radius = float(arg)
        elif opt in ("-s", "--sides"):
            sides = int(arg)
        elif opt in ("-i", "--inner"):
            inner = float(arg)
        elif opt in ("-o", "--offset"):
            offset = float(arg)
    
    # validate input
    if longitude == "" or latitude == "":
        usage(2, "Must specified both longitude and latitude in degrees\n")

    if sides == "" or sides < 3:
        usage(2, "Must give numbers of sides of polygon > 2\n")
    
    if radius == "" or radius < 0:
        usage(2, "Must specify radius > 0\n")

    # inner is different, it's optional
    if inner != "" and inner < 0:
        usage(2, "Inner radius must be positive\n")

    #
    # DO IT
    #
    if inner != "":
        # it's a star
        s = kml_star(longitude, latitude, radius, inner, sides, offset)
    else:
        s = kml_regular_polygon(longitude, latitude, radius, sides, offset)

    print s

if __name__ == "__main__":
    main(sys.argv[1:])

