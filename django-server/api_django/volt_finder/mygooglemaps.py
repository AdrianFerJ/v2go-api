"""
Instructions to run script manually:
1) launch django shell (./manage shell)
2) import this module (from volt_finder import mygooglemaps as g)
"""

import googlemaps
from datetime import datetime
import json

# Settings used by Django
#from django.conf import settings
#gmaps = googlemaps.Client(key= settings.GOOGLE_API_KEY)

# Settings to run script manually
import os
GOOGLE_API_KEY = os.getenv('v2go_GOOGLE_API_KEY')
gmaps = googlemaps.Client(key= GOOGLE_API_KEY)

# Transportation mode
mymode =  "driving" #"transit" # "walking"

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

def dumpJsonFile(jdata):
    """ Takes a json or array and ourputs into a Json File """
    with open('volt_finder/jsonDump_output.json', 'w') as json_file:
        json.dump(jdata, json_file)
    return "File saved"

def printTripSummary(direc):
    """ Takes direction service outpu as input, prints summary info"""
    print("--- Trip Info ---")
    print("From: ", direc[0]["legs"][0]["start_address"])
    print("To: ", direc[0]["legs"][0]["end_address"])
    print("Distance: ", direc[0]["legs"][0]["distance"]["text"])
    print("Duration: ", direc[0]["legs"][0]["duration"]["text"])

# Geocoding an address
# geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
# print
# # Look up an address with reverse geocoding
# reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# # Request directions via public transit
# now = datetime.now()
# directions_result = gmaps.directions("Jean Talon metro, Montreal, QC",
#                                      "Sakti gym, Montreal, QC",
#                                      mode="transit")
#                                      departure_time=now)