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
jsonDumpDir = 'volt_finder/x_scrap_stuff/jsonDump.json'
sampleCS = ["160 Rue Saint Viateur E, Montréal, QC H2T 1A8",
           "145 Mont-Royal Ave E, Montreal, QC H2T 1N9",
           "1735 Rue Saint-Denis, Montréal, QC H2X 3K4",
           "2153 Mackay St, Montreal, QC H3G 2J2",
           "3515 Avenue Lacombe, Montréal, QC H3T 1M2",
           "5265 Queen Mary Rd, Montreal, QC H3W 1Y3",
           "191 Place du Marché-du-Nord, Montréal, QC H2S 1A2",
           "1999 Mont-Royal Ave E, Montreal, QC H2H 1J4",
           "545 Milton St, Montreal, QC H2X 1W5",
           "1999 Mont-Royal Ave E, Montreal, QC H2H 1J4",
           "432 Rue Rachel E, Montréal, QC H2J 2G7"
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
class CStation:
    """CStationnt of Interest data class, for Distance Matrix output"""
    nk: str
    destination_addresses: str
    duration_txt: str
    duration_val: int
    distance_txt: str
    distance_val: int
    status: str


def format_output_cs(addr, elem):
    # formated_cs = {
    #     'nk': 'err...whats that',
    #     'destination_addresses': addr,
    #     'duration_txt': elem['duration']['text'],
    #     'duration_val': elem['duration']['value'],
    #     'distance_txt': elem['distance']['text'],
    #     'distance_val': elem['distance']['value'],
    #     'status': elem['status']                   
    # }
    # Use CStation data class object (requires serialization before the view Responds to client)
    formated_cs = CStation(
        'no_nk',
        addr, 
        elem['duration']['text'], 
        elem['duration']['value'],
        elem['distance']['text'], 
        elem['distance']['value'],
        elem['status']
    )
    return formated_cs
    

    
""" Main func """

def getDirections(departure, destination):
    """  
    Returns the directions to get from departure (A) to departure (B)
    Input: 2 locations (address or coordinates) as string 
    Output: Json formated Directions, but as an array.
    """
    now = datetime.now()
    directions_result =  gmaps.directions(
        departure, destination, mode = mymode, departure_time = now)
    return directions_result

def getNearestCS(poi, charginStations):
    """ Gets the top X nearest CS from user provided location.
    :param poi: the point of interestes, a single location provided by the user 
    :param charginStations: array of CS locations 
    """
    resp = gmaps.distance_matrix(poi, charginStations)
    
    #TODO: replace this if /else for try/except
    if resp['status']!='OK':
        return "Error"
    else:
        result = []
        for addr, elem in zip(resp['destination_addresses'], resp["rows"][0]['elements']):
            temp_CStation = format_output_cs(addr, elem)
            result.append(temp_CStation)

        # Sort CS, lower duration value first
        # sortx = sorted(top_cs, key=lambda x: x.duration_val, reverse=True)
        result.sort(key=lambda x: x.duration_val, reverse=False)
        # result.sort(key=lambda x: x['duration_val'], reverse=False)

        # Retrun top 5 results
        if len(result) > 5:
            return result[:5]
        else:
            return result  

