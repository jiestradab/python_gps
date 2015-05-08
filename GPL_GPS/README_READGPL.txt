
########################################################
                 READ GPL files 
########################################################
 usage: %s [-h|--help] <GPL file>

   
 This program reads a GPL file and writes out the following:
    
 A csv file containing time, latitude, longitude and altitude as comma-separated fields

    
 A KML file with the same information (longitude, latitude, altitude)
    (Note the difference in the order of longitude and latitude)

    
 For a given input file foo.gpl (say)

    The generated files are: foo.csv and foo.gpl


  


##########################################################################################


From:
        http://www.frontiernet.net/~werner/gps/

The format of the record is:

   
 4 bytes - status (unsigned long)
   
 4 bytes - ?????
   
 8 bytes - latitude (floating point double, decimal degrees)
 
 8 bytes - longitude (floating point double, decimal degrees)
  
 8 bytes - altitude (floating point double, meters)
    
 8 bytes - heading (floating point double, degrees)
   
 8 bytes - speed (floating point double, MPH)
    
 4 bytes - time (unsigned long, C 'time_t' type)*
  
 4 bytes - ?????

* The C 'time_t' format stores both date and time. 

The stored value is the number of seconds since January 1, 1970.

The following 'C' structure can be used to access the data in each record.

ruct GPL_Data_Point
{
    
    ULong       status;    0:3

    ULong       dummy;     4:7
    
    double      latitude;  8:15
    
    double      longitude; 16:23
    
    double      altitude;  24:31
    
    double      heading;   32:39
    
    double      speed;     40:47
    
    ULong       time;      48:51    // in <time.h format
 
    ULong       dummy3;
};

"""



by Jose Ignacio Estrada