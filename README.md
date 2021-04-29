# TwitterSquawkBot
This bot reads in data from the OpenSky API and extracts the squawk code for each aircraft. It will then send out a tweet if any emergency squawk codes are detected.

The OpenSky API is a free api and as such it should not be heavily relied on. API timeouts can and will occur and the amount of aircraft tracked globally is significantly lower than other commercial APIs that exist.

# Files
Three files for this bot are included. The first two provide two different methods to obtain data from the OpenSky API. The third is an example of the FlightRadar24 API which is significantly more reliable than OpenSky. For a quick contrast, compare the amount of global flights tracked by OpenSky as compared to FlightRadar24. At the time of writing (Thusday 8pm UTC) OpenSky tracks ~5000, while FlightRadar24 tracks ~10000.

- mainAPI.py takes advantage of the package opensky_api to make calls to the api, so running this will require the package to be installed.
- mainWeb.py uses the web API at [https://opensky-network.org/api/](https://opensky-network.org/api/) and as such does not require the OpenSky API package to run.
- fr24API.py uses the FlightRader24 API. This is not officially supported by FR24 and uses the package FlightRadarAPI. This demonstrates some of the things that you can do with this package.

An example of the tweet that this bot sends out is below.

![tweet](exampleTweet.png)
