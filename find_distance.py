import urllib.request
import json
bingMapsKey = "Ajlc9FeCH2OGYiNdqYQAZAdHkuEVx61ZrNvNzM2SA8ksjTyKdzJwuyItDffHsW0U"


def find_distance(latitude, longitude, latitude1, longitude1):


    routeUrl = "http://dev.virtualearth.net/REST/V1/Routes/Driving?wp.0=" + latitude + "," + longitude + "&wp.1=" + latitude1 + "," + longitude1 + "&key=" + bingMapsKey + "&optmz=time"

    request = urllib.request.Request(routeUrl)
    response = urllib.request.urlopen(request)

    r = response.read().decode(encoding="utf-8")
    result = json.loads(r)

    itineraryItems = result["resourceSets"][0]["resources"][0]["travelDistance"]

    return itineraryItems

