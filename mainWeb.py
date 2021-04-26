# It is critical to remember that the OpenSky API is a free API and as such is unreliable
# Squawk codes can be wrong and aircraft can be missing as the global coverage is not as good as a paid API

import requests
import json
import pandas as pd
import numpy as np
import tweepy

# Define a coordinate box if we want to restrict to a certain geographic area
lon_min, lat_min = 0, 0
lon_max, lat_max = 0, 0

# Handle twitter credentials
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Handle OpenSky API credentials
user_name = ""
password = ""

# Request data from the API
url_data = 'https://'+user_name+':'+password+'@opensky-network.org/api/states/all?'  # We can append arguments here to restrict the latitude and longitude
response = requests.get(url_data).json()

# Define a list with all the columns provided by the API
columns = ['icao24','callsign','origin_country','time_position','last_contact','long','lat','baro_altitude','on_ground','velocity',       
'true_track','vertical_rate','sensors','geo_altitude','squawk','spi','position_source']

# Create a dataframe from the request data
flights = pd.DataFrame(response['states'], columns=columns)

# Replace NaN with 0
flights = flights.fillna(0)

# Create a list with the emergency squawk codes we are looking for
squawkCodes = ["7500", "7600", "7700"]
# Scan through all flights and keep only those with emergency codes
emergencyFlights = (flights[flights["squawk"].isin(squawkCodes)])

# Extract only the values we want from the dataframe
emergencyCallsign = (emergencyFlights["callsign"])
emergencyBaroAltitude = (emergencyFlights["baro_altitude"].values)
emergencySquawk = (emergencyFlights["squawk"].values)

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
