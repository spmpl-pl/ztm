# ZTM Command-Line interface
ZTM (ZTM Warszawa) command-line interface to get timetables and vechicle locations from api.um.warszawa.pl. 

> [!IMPORTANT]
> Before using the script, please set the ZTM_API variable with command: `export ZTM_API=(apikey)`  
> You can obtain the APIKEY on https://api.um.warszawa.pl/

Usage:
`ztm action [parameters]`

## List of actions:

 - getstopid   - Looks up the Stop Group ID based on the Stop Group name.  
 - getlines    - Gets lines depaturing from the Stop. Required parameters: -i and -s.
 - getschedule - Gets a schedule of particular Line from the Stop. Required parameters: -i, -s and -l.
 - getroute    - Gets a route for a particular line. Prints all variants. Required parameters: -l.
 - getgpstram  - Gets current GPS locations for all trams on the particular line. Required parameters: -l. Optional parameters: -b.
 - getgpsbus   - Gets current GPS locations for all buses on the particular line. Required parameters: -l. Optional parameters: -b.

## List of parameters:  
  -n                Name of the Stops Group Name. For example: "Jana Kazimierza".  
  -i                Stop Group ID. For example: 5205.  
  -s                Stop ID. For example: 01.  
  -l                Line. For example: 255.  
  -b                Brigade. For example: 01.  

