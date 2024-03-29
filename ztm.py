#!/usr/bin/env python
#####################################################################################################
#####################################################################################################
##  ZTM - command line interface for accessing timetables and other information related to public  ##
##  transportation system in Warsaw, Poland.                                                       ##
##                                                                                                 ##
##  Author: Bartosz Chmielewski                                                                    ##
#####################################################################################################
#####################################################################################################
import json
import os
import argparse
import requests
import datetime
import platform

ZTM_API = str(os.getenv('ZTM_API'))
baseurl = "https://api.um.warszawa.pl/"
homedir = str(os.getenv("HOME"))
urlparams = { 'apikey': ZTM_API }
verbose = False

if platform.system() == 'Windows':
    slash = '\\'
else:
    slash = '/'



if ZTM_API == 'None':
    print("ZTM_API variable not set properly. Please set the variable with command: export ZTM_API=(apikey)")
    quit()
    
if homedir == 'None':
    print("HOME variable not set properly. Please set the variable with command: export HOME=(home directory)")
    quit()

def GetApiData(url, urlparams_local):
    ## Sending request to API and handling error codes if needed. 
    ## Input: URL and URL Parameters
    ## Output: JSON with a response

    if verbose: print(" --> Trying to connect to:", url)
    
    try:
        r = requests.get(url=url, params=urlparams_local, timeout=(5, 15))
        
    except Exception: 
    
        print(" --> ERROR! Connection to", url, "failed. Timeout.")
        print("     Please note, that the API is available only from Poland.")
        quit()
      
    else:
        if verbose: print(" --> Successfully connected to", url )
    
    if r.status_code == 200:   
        if verbose: print(" --> Connection successful. Got a response with a valid status code:", r.status_code)
           
    else:
        print(" --> ERROR! Got a response with unexpected response code:", r.status_code, ". Please try again.")
        quit()
    
    if verbose: print("")
    
    return r.json()

def GetDatabase(filepath, url, urlparams):
    ## Check if local database exists and is up to date. If not, download it from the API
    ## Input: DB file path, URL and URL parameters
    ## Output: Database as json object.  

    if ( not os.path.exists( homedir + slash + '.ztm') ):
        if verbose: print(' --> Creating directory:', homedir + slash + '.ztm' )
        os.makedirs( homedir + slash + '.ztm' )

    if( os.path.exists(filepath) and datetime.datetime.fromtimestamp(os.path.getmtime(filepath)).date() == datetime.date.today()):
        if verbose: print(" --> The database file", filepath, "is up to date...")
        if verbose: print("")

    else:
        if verbose: print(" --> The database file", filepath, "is not up to date or not existing...")        
        data = GetApiData(url, urlparams)
        with open(filepath, "w") as file:
            json.dump(data, file)
    
    try:
        f = open(filepath)
    except IOError:
        print(" --> Failed to open a database file:", filepath)
        quit()
    
    r = json.load(f)
    return r

def FindStopDetails(ParameterName, ParameterValue):
    ## Finds a Stop Group ID where the ParameterName equals to ParameterValue and return all attributes
    ## Input: ParameterName, ParameterValue
    ## Output: List of attributes for all StopIDs. 
    returnlist = []
    for a in db_busstops['result']:
        validrecord = False
        for b in a['values']:
            if ( b['key'] == ParameterName and b['value'] == ParameterValue):
                validrecord = True
                        
        if (validrecord):
            for c in a['values']:
                if c['key'] == 'slupek':
                    line = { 'StopID': (c['value']) }
                elif c['key'] == 'kierunek':
                    line |= { 'Direction': (c['value']) }
                elif c['key'] == 'szer_geo':
                    line |= { 'GPSLat': (c['value']) }
                elif c['key'] == 'dlug_geo':
                    line |= { 'GPSLon': (c['value']) }
                elif c['key'] == 'nazwa_zespolu':
                    line |= { 'StopGroupName': (c['value']) }                    
                elif c['key'] == 'id_ulicy':
                    line |= { 'StreetID': (c['value']) }     
            returnlist.append(line)
    return returnlist

def GetStopNameFromID(StopID):
    StopNames = FindStopDetails('zespol', StopID)
    if len(StopNames) > 0:
        return StopNames[0]['StopGroupName']
    else:
        print("No Stop Groups for a Given StopID...")
        quit()


def GetStopIDFromName(StopGroupName):
        returnlist = []
        urlparams_local =  urlparams
        urlparams_local |= { 'id': 'b27f4c17-5c50-4a5b-89dd-236b282bc499', 'name': args.n }
        url = baseurl + "api/action/dbtimetable_get" 

        r = GetApiData(url, urlparams_local)
        
        for i in r['result']:
            line = { 'StopGroupID': i['values'][0]['value'], 'StopGroupName': i['values'][1]['value'] }
            returnlist.append(line)
        return returnlist


parser = argparse.ArgumentParser(description="ZTM (ZTM Warszawa) command-line interface to get timetables, routes, vehicle locations and more from api.um.warszawa.pl. You can find more information including examples of use on https://github.com/spmpl-pl/ztm in README file.", epilog="Written by Bartosz Chmielewski")
parser.add_argument('action', choices=['getstop', 'getlines', 'getschedule', 'getroute', 'getgpstram', 'getgpsbus' ], help="Choose one of supported options.")
parser.add_argument('-n', nargs="?", metavar="StopGroupName", help="Name of the Stops Group Name. For example: \"Jana Kazimierza\".",)
parser.add_argument('-i', nargs="?", metavar="StopGroupID", help="Stop Group ID. For example: 5205.",)
parser.add_argument('-s', nargs="?", metavar="StopID", help="Stop ID. For example: 01.",)
parser.add_argument('-l', nargs="?", metavar="Line", help="Line. For example: 255.",)
parser.add_argument('-b', nargs="?", metavar="BrigadeID", help="Brigade. For example: 01.",)
parser.add_argument('-f', action='store_true', help="Display full schedule/Display all routes routes.",)
parser.add_argument('-v', action='store_true', default=False, help="Verbose mode.",)
args = parser.parse_args()

print("")
verbose = args.v

if args.action == 'getstop':

    urlparams_db = urlparams
    urlparams_db |= { 'id': 'ab75c33d-3a26-4342-b36a-6e5fef0a3ac3'}
    db_busstops = GetDatabase(homedir + slash + ".ztm" + slash + "ztm_busstops.json", baseurl + "api/action/dbstore_get", urlparams_db )

    if ( args.n and args.i ):
        print("Please provide either -n or -i parameters. You have provided both...")
        quit()

    elif (args.n or args.i):
        if (args.n):
            StopGroupIDs = GetStopIDFromName(args.n)
        else:
            StopGroupIDs = [ { 'StopGroupID': args.i, 'StopGroupName': GetStopNameFromID(args.i) } ]

        if( len(StopGroupIDs) == 0 ):
            print("  No Stop Groups for a given Stop Group Name...")
            quit()

        for i in StopGroupIDs:
            print("==== Stop Group Name:", i['StopGroupName'] + ". Stop Group ID:", i['StopGroupID'])
            ids = FindStopDetails('zespol', i['StopGroupID'])
            print("  == Available Stop IDs:")
            print("")
            print("  {0:<10} {1:<30} {2:<12} {3:<12} {4:<30}".format("StopID", "Direction", "GPS Lat.", "GPS Long.", "Map Link" ))
            for j in ids:
                googlelink = "https://maps.google.com/maps?q=loc:" + str(j['GPSLat']) + "," + str(j['GPSLon'])
                print("  {0:<10} {1:<30} {2:<12} {3:<12} {4:<30}".format(j['StopID'], j['Direction'], j['GPSLat'], j['GPSLon'], googlelink ))
            print("")

    else:

        print("Please provide a Stop Group Name with -n parameter or Stop Group ID with -i parameter.")
        print("")
        print("Examples:")
        print("  - ztm getstop -n \"Jana Kazimierza\"")
        print("  - ztm getstop -i 7006")

elif args.action == 'getlines':

    urlparams_db = urlparams
    urlparams_db |= { 'id': 'ab75c33d-3a26-4342-b36a-6e5fef0a3ac3'}
    db_busstops = GetDatabase(homedir + slash + ".ztm" + slash + "ztm_busstops.json", baseurl + "api/action/dbstore_get", urlparams_db )

 
    if ( args.n and args.i ):
        print("Please provide either -n or -i parameters. You have provided both...")
        quit()

    elif ( ( args.n or args.i ) ):
        
        if(args.n):
            StopGroupIDs = GetStopIDFromName(args.n)
        else:
            StopGroupIDs = [ { 'StopGroupID': args.i, 'StopGroupName': GetStopNameFromID(args.i) } ]

        if ( len(StopGroupIDs) == 0 ):
            print("No Stop Groups for a given Stop Group Name...")
            quit()            

        for i in StopGroupIDs:
            
            if( args.s ):
                ids = [ { 'StopID': args.s, 'Direction': 'N/A' } ]
            else:
                ids = FindStopDetails('zespol', i['StopGroupID'])
            
            print("==== Stop Group Name:", i['StopGroupName'] + ". Stop Group ID:", i['StopGroupID'] )
            print("")
            
            for k in ids:
            
                urlparams |= { 'id': '88cd555f-6f31-43ca-9de4-66c479ad5942', 'busstopId': i['StopGroupID'] , 'busstopNr': k['StopID'] }
                url = baseurl + "api/action/dbtimetable_get" 
                r = GetApiData(url, urlparams)

                print("  == Stop ID:", k['StopID'] + ". Direction:", k['Direction'])

                if( len( r['result'] ) > 0 ):
                    
                    lineslist = ''
                    firstline = True
                    for j in r['result']:
                        try:
                            line = j['values'][0]['value']
                        except TypeError:
                            print("No such Stop ID in the database")
                            quit()    
                        if firstline:
                            lineslist = line
                            firstline = False
                        else:
                            lineslist += ', ' + line
                    print("  Lines:", lineslist)
                    
                    
                else:
                    print("  No lines on this Stop.")
                
                print("")
    
    else:

        print("Please provide Stop Group ID with -i or Stop Group Name with -n and optionally Stop ID with -s parameters.")
        print("")
        print("Examples:")
        print("  - ztm getlines -n \"Okopowa\"")
        print("  - ztm getlines -i 5205 -s 01")
        print("  - ztm getlines -n \"Metro Politechnika\" -s 01")


elif args.action == 'getschedule':

    urlparams_db = urlparams
    urlparams_db |= { 'id': 'ab75c33d-3a26-4342-b36a-6e5fef0a3ac3'}
    db_busstops = GetDatabase(homedir + slash + ".ztm" + slash + "ztm_busstops.json", baseurl + "api/action/dbstore_get", urlparams_db )


    if ( args.n and args.i ):
        print("Please provide either -n or -i parameters. You have provided both...")
        quit()

    if ( ( args.n or args.i ) and args.s and args.l ):
        
        if(args.n):
            StopGroupIDs = GetStopIDFromName(args.n)
        else:
            StopGroupIDs = [ { 'StopGroupID': args.i, 'StopGroupName': GetStopNameFromID(args.i) } ]
 
        if ( len(StopGroupIDs) == 0 ):
            print("No Stop Groups for a given Stop Group Name...")
            quit()   
            
        for i in StopGroupIDs:    
            
            urlparams_local = urlparams
            urlparams_local |= { 'id': 'e923fa0e-d96c-43f9-ae6e-60518c9f3238', 'busstopId': i['StopGroupID'], 'busstopNr': args.s, 'line': args.l }
            url = baseurl + "api/action/dbtimetable_get" 
            r = GetApiData(url, urlparams_local)
            print("==== Schedule for line:", args.l + ". Stop Group Name:", i['StopGroupName'] + ". Stop Group ID:", i['StopGroupID'])
            print("")    

            if (len(r['result']) > 0 ):
                if( args.f ):

                    print("{0:<10} {1:<35} {2:<10}".format("Time", "Direction" , "Brigade"))

                    for j in r['result']:
                        hour = j['values'][5]['value'][0:2]
                        minutes = j['values'][5]['value'][3:5]
                        print("{0:<10} {1:<35} {2:<10}".format(str(int(hour)%24).zfill(2) + ':' + minutes, j['values'][3]['value'], j['values'][2]['value'] ))

                else:
                
                    timetable = ["" for x in range(30)]
                    
                    for j in r['result']:
                        hour = j['values'][5]['value'][0:2]
                        minutes = j['values'][5]['value'][3:5]
                        timetable[int(hour)] += minutes + " "
                    
                    hour = 0
                    
                    for j in timetable:
                        if ( not j == "" ):
                            print(str(hour % 24).zfill(2) + ': ', j)
                        hour += 1
                    
                    print("")
                    print("Hint: You can print a schedule with Directions and Brigades with -f parameter...")

            else:

                print("==== No results...")
                print("")
 
    else:

        print("Please provide Stop Group ID with -i or Stop Group Name with -n and Stop ID with -s and Line with -l parameters.")
        print("")
        print("Examples:")
        print("  - ztm getschedule -i 5205 -s 01 -l 255 -f")
        print("  - ztm getschedule -n \"Jana Kazimierza\" -s 01 -l 255")

elif args.action == 'getroute':

    if ( args.l ):

        url = baseurl + "api/action/public_transport_routes" 

        db_routes = GetDatabase( homedir + slash + ".ztm" + slash + "ztm_routes.json", baseurl + "api/action/public_transport_routes", urlparams)
        db_dictionary = GetDatabase( homedir + slash + ".ztm" + slash + "ztm_dictionary.json", baseurl + "api/action/public_transport_dictionary", urlparams)
        urlparams_local = urlparams
        urlparams_local |= { 'id': 'ab75c33d-3a26-4342-b36a-6e5fef0a3ac3'}
        db_busstops = GetDatabase(homedir + slash + ".ztm" + slash + "ztm_busstops.json", baseurl + "api/action/dbstore_get", urlparams_local )

        try:
            db_routes_line = db_routes['result'][args.l]

        except KeyError:
            print("No such line in the database")
            quit()

        #print("")
        print("==== There are", len(db_routes_line), "route variants for the line", str(args.l) + ".")
        if( args.f ):
            print("==== Printing all variants...")
        else:
            print("==== Printing only primary routes and detours. Use -f parameter to print all variants.")
            
        for i in db_routes_line:
            
            if (args.f or ( str(i)[:2] == 'TP' or str(i)[:2] == 'TO' )):
              
                noofstops = len(db_routes_line[i])  
                print("")
                print("==== Route variant ID:", str(i) + ". Number of Stops:", noofstops)
                print("")
                print("  {0:<5} {1:<30} {2:<10} {3:<20} {4:<15} {5:<15}".format("No", "Stop Name", "Stop ID", "Stop Type", "Distance", "Street"))
                
                n=1
                for j in db_routes_line[i]:
                    nstr=str(n)

                    StopNameID = db_routes_line[i][nstr]['nr_zespolu']
                    StopName = GetStopNameFromID(StopNameID)
                    StopID=db_routes_line[i][nstr]['nr_przystanku']
                    StopType=db_dictionary['result']['typy_przystankow'][db_routes_line[i][nstr]['typ']]
                    Distance=db_routes_line[i][nstr]['odleglosc']
                    StreetName=db_dictionary['result']['ulice'][db_routes_line[i][nstr]['ulica_id']]
                    print("  {0:<5} {1:<30} {2:<10} {3:<20} {4:<15} {5:<15}".format(nstr, StopName, StopID, StopType, Distance, StreetName))
                    n += 1

                print("")
    else:
        print("Please provide Line with -l parameter. Example: ztm getroute -l 255")
        print("")
        print("Examples:")
        print("  - ztm getroute -l 255")


elif args.action == 'getgpstram' or args.action == 'getgpsbus':

    if args.action == 'getgpsbus':  type = '1'
    else:   type = '2'
    
    if ( args.l ):

        urlparams_local = urlparams
        urlparams_local |= {  'resource_id': 'f2e5503e927d-4ad3-9500-4ab9e55deb59', 'type': type, 'line': args.l }
        url = baseurl + "api/action/busestrams_get" 

        if ( args.b ):  urlparams_local |= { 'brigade': args.b }
   
        r = GetApiData(url, urlparams_local)

        print("{0:<22} {1:<8} {2:<10} {3:<12} {4:<12} {5:<12} {6:<30}".format("Last update", "Line", "Brigade", "Vehicle ID", "GPS Lat.", "GPS Long.", "Map link"))
        for i in r['result']:
            googlelink = "https://maps.google.com/maps?q=loc:" + str(i['Lat']) + "," + str(i['Lon'])
            print("{0:<22} {1:<8} {2:<10} {3:<12} {4:<12} {5:<12} {6:<30}".format(i['Time'], i['Lines'], i['Brigade'], i['VehicleNumber'], i['Lat'], i['Lon'], googlelink))
    
    else:
        
        print("Please provide Line with -l and optionally brigade with -b parameters.")
        print("")
        print("Examples:")
        print("  - ztm getgpstram -l 7")
        print("  - ztm getgpsbus -l 523")
        
