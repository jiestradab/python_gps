#!/usr/bin/python
#

"""

    from:
        http://www.frontiernet.net/~werner/gps/

the format of the record is:

    4 bytes - status (unsigned long)
    4 bytes - ?????
    8 bytes - latitude (floating point double, decimal degrees)
    8 bytes - longitude (floating point double, decimal degrees)
    8 bytes - altitude (floating point double, meters)
    8 bytes - heading (floating point double, degrees)
    8 bytes - speed (floating point double, mph)
    4 bytes - time (unsigned long, c 'time_t' type)*
    4 bytes - ?????

* the c 'time_t' format stores both date and time. the stored value is the number of seconds since january 1, 1970.

the following 'c' structure can be used to access the data in each record.

struct gpl_data_point
{
    ulong       status;    0:3
    ulong       dummy;     4:7
    double      latitude;  8:15
    double      longitude; 16:23
    double      altitude;  24:31
    double      heading;   32:39
    double      speed;     40:47
    ulong       time;      48:51    // in <time.h format
    ulong       dummy3;
};

"""

import os
import struct
import sys
import time



reclength = 56

usage_msg = """
    usage: %s [-h|--help] <gpl file>

    this program reads a gpl file and writes out the following:
    a csv file containing time, latitude, longitude and altitude as comma-separated fields

    a kml file with the same information (longitude, latitude, altitude)
    (note the difference in the order of longitude and latitude)

    for a given input file foo.gpl (say)

    the generated files are: foo.csv and foo.gpl


    """ % (sys.argv[0], )


column_hdr_format = '%20s, %15s, %15s, %15s\n'

column_format = '%20s, %15lf, %15lf, %15lf\n'


if len(sys.argv) < 2:
    print usage_msg
    sys.exit(1)

if sys.argv[1] == "-h" or sys.argv[1] == "--help":
    print usage_msg
    sys.exit(0)


myfile = sys.argv[1]

# foo.txt -> ('foo', '.txt')
bname = os.path.splitext(os.path.basename(myfile))[0]
csvfile = bname + '.csv'
kmlfile = bname + '.kml'

if not os.path.isfile(myfile):
    print "file %s should be a regular file\n" % myfile
    sys.exit(1)

try:
    fdcsv = open(csvfile, 'w')
    fdkml = open(kmlfile, 'w')

except ioerror as e:
    print "i/o error({0}): {1}".format(e.errno, e.strerror)
    sys.exit(1)

fdcsv.write(column_hdr_format % ("latitude", "longitude", "altitude"))

fdkml.write("<?xml version='1.0' encoding='utf-8'?>\n")
fdkml.write("<kml xmlns='http://earth.google.com/kml/2.1'>\n")
fdkml.write("<document>\n")
fdkml.write("   <name>" + kmlfile +"</name>\n")


with open(myfile, "rb") as f:
        bytes = f.read(reclength)
        while len(bytes) == reclength :
            # do stuff with byte.
            latitude = struct.unpack('d', bytes[8:16])[0]
            longitude = struct.unpack('d', bytes[16:24])[0]
            altitude = struct.unpack('d', bytes[24:32])[0]
            mytime = struct.unpack('l', bytes[48:52])[0]

            timetup = time.localtime(mytime * 1.0)
            # let's convert the time to yyyy-mm-dd hh:mm:ss format
            mytimestr = time.strftime('%y-%m-%d %h:%m:%s', timetup)

            # fdcsv.write("%10f, %15lf, %15lf, %15lf\n" % (mytime, latitude, longitude, altitude))
            fdcsv.write(column_format % (mytimestr, latitude, longitude, altitude))

            fdkml.write("   <placemark>\n")
            fdkml.write("       <name>" + str(mytimestr) + "</name>\n")
            fdkml.write("       <description>" + "polito" + "</description>\n")
            fdkml.write("       <point>\n")
            fdkml.write("           <coordinates>" + "%15lf, %15lf, %15lf" % (longitude, latitude, altitude) + "</coordinates>\n")
            fdkml.write("       </point>\n")
            fdkml.write("   </placemark>\n")

            bytes = f.read(reclength)


# add suffix
fdkml.write("</document>\n")
fdkml.write("</kml>\n")

print "\n\ngenerated files: %s and %s from gpl file: %s\n" % (csvfile, kmlfile, myfile)

fdcsv.close()
fdkml.close()

