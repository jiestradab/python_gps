"""latitude longitude height from a NMEA Log
 GGA 'Time','Latitude','Longitude','Q_fix','Num_Sats','Num_Sats','HDOP','Altitude'"""
import re
lat=[]
lon=[]
he=[]
COLUMN_HDR_FORMAT = '%10s %15s, %15s, %15s\n'
COLUMN_FORMAT = '%10d, %15lf, %15lf, %15lf\n'
#Initizialization kml file
nombre="my first kml"
fdkml = open("kmlfile.kml", 'w')
fdcsv = open("csvfile.txt", 'w')
fdcsv.write(COLUMN_HDR_FORMAT % ("Nun", "Latitude", "Longitude", "Altitude"))
fdkml.write("<?xml version='1.0' encoding='UTF-8'?>\n")
fdkml.write("<kml xmlns='http://earth.google.com/kml/2.1'>\n")
fdkml.write("<Document>\n")
fdkml.write("   <name>" +nombre+"</name>\n")
count=0
with open("log_ST8_20140701_030657.txt", 'r') as f:
        for line in f:
                current= line.split(',')
                print current
                m=re.match("^\$GPGGA",current[0])
                print m
                if m:
                    aux_lat=current[2]
                    process_lat=float(aux_lat[:2])+float(aux_lat[2:])/60
                    if current[3]!='N':
                        process_lat=process_lat*-1
                    aux_lon=current[4]
                    process_lon=float(aux_lon[:3])+float(aux_lon[3:])/60
                    lat.append(process_lat)
                    lon.append(process_lon)
                    aux_he=float(current[9])
                    he.append(aux_he)
                    count+=1
                    fdcsv.write(COLUMN_FORMAT % (count, process_lat, process_lon, aux_he))
                    fdkml.write("   <Placemark>\n")
                    fdkml.write("       <name>" + str(count) + "</name>\n")
                    fdkml.write("       <description>" + "Polito" + "</description>\n")
                    fdkml.write("       <Point>\n")
                    fdkml.write("           <coordinates>" + "%10f, %10f," % (process_lon, process_lat) + "</coordinates>\n")
                    fdkml.write("       </Point>\n")
                    fdkml.write("   </Placemark>\n")

fdkml.write("</Document>\n")
fdkml.write("</kml>\n")
print lat
print lon
print he
f.close()
fdkml.close()
fdcsv.close()
