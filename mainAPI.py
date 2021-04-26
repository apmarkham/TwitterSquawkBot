# It is critical to remember that the OpenSky API is a free API and as such is unreliable
# Squawk codes can be wrong and aircraft can be missing as the global coverage is not as good as a paid API

import pandas as pd
import tweepy 
from opensky_api import OpenSkyApi

# Handle OpenSky API and Twitter API credentials
consumer_key = '' 
consumer_secret = '' 
access_token = '' 
access_token_secret = ''
api = OpenSkyApi("", "")

states = api.get_states()
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Initialise a dictionary with keys where we will store the emergency flight data
emergencyFlights = {'callsign' : [], 'squawk': [], 'baro_altitude': []}

# Loop through all state vectors and identify those with emergency squawk codes
for s in states.states:
    if s.squawk == "7500" or s.squawk == "7600" or s.squawk == "7700":
        emergencyFlights["callsign"].append(s.callsign)
        emergencyFlights["squawk"].append(s.squawk)
        emergencyFlights["baro_altitude"].append(s.baro_altitude)

# Extract all the values from the dictioary into seperate lists
emergencyCallsign = emergencyFlights.get("callsign")
emergencySquawk = emergencyFlights.get("squawk")
emergencyBaroAltitude = emergencyFlights.get("baro_altitude")

# Strip all whitespaces from the list of strings
emergencyCallsign = [s.strip() for s in emergencyCallsign]

# Sometimes the altitude will be "None" (NoneType element) when the aircraft is on the ground. We need to change these None values to zero.
emergencyBaroAltitude = [0 if item is None else item for item in emergencyBaroAltitude]

# Convert altitude in metres to feet, forcing an integer value
emergencyBaroAltitude = [int(i * 3.28084) for i in emergencyBaroAltitude]

# Loop through the number of emergency squawk codes currently present and display aircraft information for each one
for i in range(len(emergencySquawk)):
    print("Current emergency. Callsign %s, current barometric altitude %sft, squawk %s." % (emergencyCallsign[i], emergencyBaroAltitude[i], emergencySquawk[i]))

# This function will check if any emergency squawk codes exist and then send out a tweet for each emergency
def postTweet():
    if len(emergencySquawk) > 0:
        for i in range(len(emergencySquawk)):
            tweettopublish = ("Current emergency. Callsign %s, current barometric altitude %sft, squawk %s." % (emergencyCallsign[i], emergencyBaroAltitude[i], emergencySquawk[i]))
            api.update_status(tweettopublish)

tweettopublish = ""
postTweet()
