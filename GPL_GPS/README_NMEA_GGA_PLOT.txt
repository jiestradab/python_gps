NMEA GGA MESSAGE
$GPGGA,HHMMSS.SS,DDMM.MMMMM,K,DDDMM.MMMMM,L,N,QQ,PP.P,AAAA.AA,M,±XX.XX,M,
SSS,RRRR*CC<CR><LF>

from http://hemispheregnss.com/gpsreference/GPGGA.htm

1. The script read the message GGA and extract latitude, longitude and height.
2. Create a kml file and add each fix to the same file.
3  Create a txt file with the LLH.

By Jose Ignacio Estrada 