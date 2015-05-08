__author__ = 'Jose Ignacio Estrada'
from pynmea import nmea
import matplotlib.pyplot as plt
import serial
import re
import sys

def readBuffer():
    try:
        data = device.read(1)
        n = device.inWaiting()
        if n:
            data = data + device.read(n)

        return data
    except Exception, e:
        print "Big time read error, what happened: ", e
        sys.exit(1)


lat_list = []
lon_list = []
alt_list= []
# reset_command="$PSRF101,0,0,0,0,0,0,12,4*10" #command to cold start the receiver
device = serial.Serial(port="COM6", baudrate=4800, timeout=5)
#device.write(reset_command)
line = ""
newdata = ""
count = 0
while device.isOpen():


    if newdata:
        line = newdata
        newdata = ""
    line = line + readBuffer()
    if re.search("\r\n", line):
        data, newdata = line.split("\r\n")
        if re.match("^\$GPGGA", data):
            count += 1
            gpgga = nmea.GPGGA()
            gpgga.parse(data)
            aux_lat = gpgga.latitude
            f_aux_lat = float(aux_lat[:2]) + float(aux_lat[2:]) / 60
            aux_lon = gpgga.longitude
            f_aux_lon = float(aux_lon[:3]) + float(aux_lon[3:]) / 60
            lat_list.append(f_aux_lat)
            lon_list.append(f_aux_lon)
            aux_alt=gpgga.antenna_altitude
            alt_list.append(aux_alt)
            print data
            print alt_list
            if count == 5:
                device.write("$PSRF101,0,0,0,0,0,0,12,4*10")####cold start for BU353-S4. It needs to be identified.
                device.close()

        line = ""

fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.scatter(x=lat_list,y=lon_list) #plot each point
#axis is autoscaled
ax1.axis((37.5,38,122,122.5))
plt.ylabel('longitude')
plt.xlabel('latitude')
plt.title('Latitude vs longitude')
fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.scatter(x=range(len(alt_list)), y=alt_list, s = 1, c='r')
plt.ylabel('meters')
plt.xlabel('counts')
plt.title('ALTITUDE')
plt.show()
