"""
Instructions to run script manually:
1) launch django shell (./manage shell)
2) import this module (from volt_finder import mygooglemaps as g)
"""

import googlemaps
from datetime import datetime
import json
from dataclasses import dataclass

# Settings used by Django
#from django.conf import settings
#gmaps = googlemaps.Client(key= settings.GOOGLE_API_KEY)

# Settings to run script manually
import os
GOOGLE_API_KEY = os.getenv('v2go_GOOGLE_API_KEY')
gmaps = googlemaps.Client(key= GOOGLE_API_KEY)

# Transportation mode
mymode =  "driving" #"transit" # "walking"
jsonDumpDir = 'volt_finder/scrap_stuff/jsonDump.json'
sampleCS = ["160 Rue Saint Viateur E, Montréal, QC H2T 1A8",
           "145 Mont-Royal Ave E, Montreal, QC H2T 1N9",
           "1735 Rue Saint-Denis, Montréal, QC H2X 3K4",
           "2153 Mackay St, Montreal, QC H3G 2J2",
           "3515 Avenue Lacombe, Montréal, QC H3T 1M2",
           "5265 Queen Mary Rd, Montreal, QC H3W 1Y3"
]

""" Helpers """
def printParams():
    print("--- Params ---")
    print("Transport mode: ", mymode)
    print("Json dump directory: ", jsonDumpDir)
    print("Sample CS: ", sampleCS)

def dumpJsonFile(jdata):
    """ Takes a json or array and ourputs into a Json File """
    with open(jsonDumpDir, 'w') as json_file:
        json.dump(jdata, json_file)
    return "File saved"

def printTripSummary(direc):
    """ Takes direction service outpu as input, prints summary info"""
    print("--- Trip Info ---")
    print("From: ", direc[0]["legs"][0]["start_address"])
    print("To: ", direc[0]["legs"][0]["end_address"])
    print("Distance: ", direc[0]["legs"][0]["distance"]["text"])
    print("Duration: ", direc[0]["legs"][0]["duration"]["text"])

@dataclass
class POI:
    """Point of Interest data class, for Distance Matrix output"""
    destination_addresses: str
    duration_txt: str
    duration_val: int
    distance_txt: str
    distance_val: int
    status: str
    
""" Main func """
def getDirections(departure, destination):
    """ 
    Returns the directions to get from departure (A) to departure (B)
    Input: 2 locations (address or coordinates) as string 
    Output: Json formated Directions, but as an array.
    """
    now = datetime.now()
    directions_result =  gmaps.directions(departure,
                                        destination,
                                        mode = mymode,
                                        departure_time = now
    )
    return directions_result

def getNearestCS(poi, charginStations=None):
    """ Gets the top X nearest CS from user provided location.

    :param poi: the point of interestes, a single location provided by the user 
    :param charginStations: array of CS locations 
    """
    if charginStations == None:
        charginStations = sampleCS

    resp = gmaps.distance_matrix(poi, charginStations)
    
    if resp['status']!='OK':
        return "Error"
    else:
        result = []
        for addr, elem in zip(resp['destination_addresses'], resp["rows"][0]['elements']):
            result.append(POI(addr, 
                            elem['duration']['text'], 
                            elem['duration']['value'],
                            elem['distance']['text'], 
                            elem['distance']['value'],
                            elem['status']
            ))
        # Can also slice list to return top x results (aka. result[0:x])
        return  result  

    

# SCRAP
#for i in r["rows"][0]['elements']:
# element duration value = r["rows"][0]['elements'][0]['duration']['value']
# destination_addresses  = r['destination_addresses'][0]

