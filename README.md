# TwitterSquawkBot
This bot reads in data from the OpenSky API and extracts the squawk code for each aircraft. It will then send out a tweet if any emergency squawk codes are detected.

The OpenSky API is a free api and as such it should not be heavily relied on. API timeouts can and will occur and the amount of aircraft tracked globally is significantly lower than other commercial APIs that exist.

# Files
Two files for this bot are included. These files provide two different methods to obtain data from the OpenSky API.

- mainAPI.py takes advantage of the package opensky_api to make calls to the api, so running this will require the package to be installed.
- mainWeb.py uses the web API at [https://opensky-network.org/api/](https://opensky-network.org/api/) and as such does not require the OpenSky API package to run.

Another way to approach this is to use FlightRadar24 data. The FlightRadar24 API is significantly more reliable than OpenSky data. For a quick contrast, compare the amount of global flights tracked by OpenSky as compared to FlightRadar24. At the time of writing (Thusday 8pm UTC) OpenSky tracks ~5000, while FlightRadar24 tracks ~10000.

However, accessing the FlightRadar24 free API will not return more than 1500 flights per call, and while this could be circumvented by making multiple calls and ignoring aircraft that you already have data for, it is not a good idea to hammer the API like this. Thus an example of this has not been included.

An example of the tweet that this bot sends out is below.

![tweet](exampleTweet.png)
