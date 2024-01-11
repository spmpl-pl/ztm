# ZTM Command-Line interface
ZTM (ZTM Warszawa) command-line interface to get timetables and vechicle locations from api.um.warszawa.pl. 

Before using the script, please set the ZTM_API variable with command: `export ZTM_API=(apikey)`
You can obtain the APIKEY on https://api.um.warszawa.pl/

Usage:
`ztm action [parameters]`

List of parameters:
  -n                Name of the Stops Group Name. For example: "Jana Kazimierza".
  -i                Stop Group ID. For example: 5205.
  -s                Stop ID. For example: 01.
  -l                Line. For example: 255.
  -b                Brigade. For example: 01.

