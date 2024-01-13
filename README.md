# ZTM Command-Line interface
ZTM (ZTM Warszawa) command-line interface to get timetables, routes, vehicle locations and more from api.um.warszawa.pl. The project is written in python as a one file program. 

> [!IMPORTANT]
> Before using the script, please set the ZTM_API variable with command: `export ZTM_API=(apikey)`  
> You can obtain the APIKEY on https://api.um.warszawa.pl/

### Usage:
`ztm action [parameters]`

### Example commands:

 - `ztm getstopid -n "Centrum"` - gets valid Stop Group IDs for a give Stop Group Name. 
 - `ztm getlines -i 7013 -s 01` - gets lines for a given Stop Group ID and Stop ID. 
 - `ztm getschedule -i 7013 -s 01 -l 525` - gets schedule for a given Stop Group ID, Stop ID and Line.
 - `ztm getroute -l 255` - gets all routes for a given Line.
 - `ztm getgpstram -l 1` - show all trams for a given line with GPS locations. 
 - `ztm getgpsbus -l 523` - show all buses for a given line with a GPS locations. 

## List of actions:
| Action | Description |
| --- | --- |
| `getstopid` | Looks up the Stop Group ID based on the Stop Group name. |
| `getlines` | Gets lines depaturing from the Stop. Required parameters: -i and -s. |
| `getschedule` | Gets a schedule of particular Line from the Stop. Required parameters: -i, -s and -l. |
| `getroute` | Gets a route for a particular line. Prints all variants. Required parameters: -l.|
| `getgpstram` | Gets current GPS locations for all trams on the particular line. Required parameters: -l. Optional parameters: -b. |
| `getgpsbus` | Gets current GPS locations for all buses on the particular line. Required parameters: -l. Optional parameters: -b. |

## List of parameters:  
| Option | Description |
| --- | --- |
| `-n` | Name of the Stops Group Name. For example: "Jana Kazimierza". |
| `-i` | Stop Group ID. For example: 5205. |
| `-s` | Stop ID. For example: 01. |
| `-l` | Line. For example: 255. |
| `-b` | Brigade. For example: 01. |

